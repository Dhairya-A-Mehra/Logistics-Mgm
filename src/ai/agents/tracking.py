"""Tracking agent factory.

This module avoids importing the higher-level LangChain agent helpers at
module-import time because those APIs vary between LangChain releases and
can raise ImportError which prevents the whole application from starting.

Instead we provide a get_tracking_agent_executor() factory which attempts to
build a proper tool-calling AgentExecutor at runtime and falls back to a
simple LLM-only executor if the LangChain helper is not available.
"""

from typing import Any, Dict

from .shared import llm  # keep the project's shared LLM
from ..tools.database import get_shipment_status

# Tools list (kept lightweight so module import is safe)
tools = [get_shipment_status]


class _FallbackExecutor:
    """A minimal executor used when the LangChain agent factory isn't
    available. It simply calls the underlying LLM and returns a dict with
    a single 'output' key so callers keep the same shape.
    """

    def __init__(self, llm):
        self.llm = llm

    def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        user_input = payload.get("input") or ""
        # Try common LLM call styles
        if hasattr(self.llm, "predict"):
            out = self.llm.predict(user_input)
        elif hasattr(self.llm, "__call__"):
            out = self.llm(user_input)
        elif hasattr(self.llm, "generate"):
            # generate may return a complex object; try to coerce
            gen = self.llm.generate([user_input])
            try:
                out = gen.generations[0][0].text
            except Exception:
                out = str(gen)
        else:
            out = ""
        return {"output": out}


def get_tracking_agent_executor():
    """Return an executor-like object with an `invoke` method.

    This will try to construct a real AgentExecutor using the installed
    LangChain utilities. If that fails (ImportError or API mismatch), it
    returns a lightweight fallback implementation so the app can keep
    running.
    """
    try:
        # Use importlib to avoid static analyzer warnings for optional/langchain
        import importlib

        prompts_mod = None
        try:
            prompts_mod = importlib.import_module("langchain_core.prompts")
        except Exception:
            try:
                prompts_mod = importlib.import_module("langchain.prompts")
            except Exception:
                prompts_mod = None

        if prompts_mod is None:
            raise ImportError("no ChatPromptTemplate implementation found")

        ChatPromptTemplate = getattr(prompts_mod, "ChatPromptTemplate")

        agents_mod = importlib.import_module("langchain.agents")
        create_tool_calling_agent = getattr(agents_mod, "create_tool_calling_agent")
        AgentExecutor = getattr(agents_mod, "AgentExecutor")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful tracking assistant for the LogiMAS system. You have access to a tool that can look up shipment information. Only use the tool if a valid shipment ID is provided in the user's query.",
                ),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        tool_calling_agent = create_tool_calling_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=tool_calling_agent, tools=tools, verbose=False)
        return executor
    except Exception as exc:  # pragma: no cover - defensive fallback
        print("[warning] could not build LangChain tool-calling agent; using fallback. Error:", exc)
        return _FallbackExecutor(llm)


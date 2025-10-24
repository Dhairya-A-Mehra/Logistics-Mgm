"""Cost agent factory with lazy imports and fallback.

Provides get_cost_agent_executor() which returns an object with invoke(payload).
"""

from typing import Any, Dict

from .shared import llm
from ..tools.database import calculate_route_fuel_cost

tools = [calculate_route_fuel_cost]


class _FallbackExecutor:
    def __init__(self, llm):
        self.llm = llm

    def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        user_input = payload.get("input") or ""
        if hasattr(self.llm, "predict"):
            out = self.llm.predict(user_input)
        elif hasattr(self.llm, "__call__"):
            out = self.llm(user_input)
        elif hasattr(self.llm, "generate"):
            gen = self.llm.generate([user_input])
            try:
                out = gen.generations[0][0].text
            except Exception:
                out = str(gen)
        else:
            out = ""
        return {"output": out}


def get_cost_agent_executor():
    try:
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
                    "You are a cost optimization analyst for LogiMAS. Your primary function is to calculate the fuel cost for shipments using your available tool. When asked about cost, provide a clear summary including the distance, fuel type, and the final estimated cost.",
                ),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_tool_calling_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
        return executor
    except Exception as exc:  # pragma: no cover - defensive
        print(
            "[warning] could not build cost LangChain agent; using fallback. Error:",
            exc,
        )
        return _FallbackExecutor(llm)

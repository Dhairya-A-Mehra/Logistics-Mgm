from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ...ai.graph import agent_graph  # Import from src/ai/
from ...ai.schemas.graph_state import AgentState

# from api.dependencies import get_current_user  # Use existing security if needed

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def run_ai_query(request: QueryRequest):
    state = AgentState(initial_query=request.query, intermediate_steps=[])
    result = agent_graph.invoke(state)
    return {"response": result["final_response"]}

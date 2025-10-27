from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ...ai.graph import agent_graph  # Import from src/ai/
from ...ai.schemas.graph_state import AgentState

# from api.dependencies import get_current_user  # Use existing security if needed

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
async def run_ai_query(request: QueryRequest):
    try:
        state = AgentState(initial_query=request.query, intermediate_steps=[])
        result = agent_graph.invoke(state)
        return {"response": result.get("final_response", "No response generated")}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return {"error": f"Error processing your request: {str(e)}"}

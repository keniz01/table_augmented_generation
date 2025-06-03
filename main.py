from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from time import localtime, strftime

import uvicorn

from src.agents.database_agent import DatabaseAgent
from src.database_utils import DatabaseUtils
from src.llm_models.instruction_model import InstructionModel
from src.llm_models.embedding_model import EmbeddingModel

# Initialize models and agent
llm_model = InstructionModel()
db_utils = DatabaseUtils()
embedding_model = EmbeddingModel()
agent = DatabaseAgent(llm_model, embedding_model, db_utils)

# Create FastAPI app
app = FastAPI(
    title="Database Query API",
    description="API for querying a database using LLM agents.",
    version="1.0.0"    
)

# Define request body model
class QueryRequest(BaseModel):
    query: str

# Define response model (optional)
class QueryResponse(BaseModel):
    response: str
    start_time: str
    end_time: str

@app.post("/query", response_model=QueryResponse)
async def query_database(request: QueryRequest):
    try:
        start_time = strftime("%H:%M:%S", localtime())
        response = agent.invoke(request.query)
        end_time = strftime("%H:%M:%S", localtime())
        return QueryResponse(response=response, start_time=start_time, end_time=end_time)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Bootstrap server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

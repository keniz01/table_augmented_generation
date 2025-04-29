from time import localtime, strftime
from agents.database_agent import DatabaseAgent
from database_utils import DatabaseUtils
from llm_models.instruction_model import InstructionModel
from llm_models.embedding_model import EmbeddingModel

llm_model=InstructionModel()
db_utils=DatabaseUtils()
embedding_model=EmbeddingModel()

if __name__ == "__main__":
    try:
        start_time=strftime("%H:%M:%S", localtime())
        agent=DatabaseAgent(llm_model,embedding_model,db_utils)
        response=agent.invoke('List the top 10 tracks by Sizzla')
        end_time=strftime("%H:%M:%S", localtime())
        print(f"Response Time: {start_time} to {end_time}")
        print(response)
    except (Exception) as error:
        print('ERROR: ',error)

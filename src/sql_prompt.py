from os import path
import sys

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

from src.prompt_base import AbstractPrompt
from src.prompt_template import PromptTemplate
      
class SqlPrompt(AbstractPrompt):

    def __init__(self):
        super().__init__()

    def generate_prompt(self, context:str, question: str) -> str:
        return f"""<|system|>You must use the context to generate a correct Postgres SQL statement to answer the question at the end.
Strictly only use table and column names defined in the context and ayou must use both table and column aliases.
If the question does not make sense or you dont know the answer just say "I dont know".
You must only return valid SQL - do not return explanations, advice or assumptions.<|end|>
<|user|>
Count albums distributed by record label 'Greenesleeves'<|end|>
<|assistant|>
select count(a.*) album_count 
from album a 
inner join record_label rl on rl.label_id = a.label_id 
where rl.label_name ILIKE 'Greensleeves Records';<|end|>
<|user|>
How many albums does the recording artist 'Gregory Isaacs' have?<|end|>
<|assistant|>
SELECT COUNT(al.*) 
FROM album al;<|end|>
<|user|>
Show all tracks on the album 'Soca Xplosion 2007' have?<|end|>
<|assistant|>
SELECT tr.track_id, tr.title, tr.duration, tr.position, tr.release_year, tr.genre_id, tr.label_id, tr.artist_id, tr.album_id 
FROM track tr
INNER JOIN album al on al.album_id=tr.album_id 
WHERE al.title ILIKE 'Soca Xplosion';<|end|>
<|user|>
Context: {context}
Question: {question}
<|end|>
<|assistant|>"""
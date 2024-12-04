# gpt_handler.py
from openai import OpenAI
from openai import OpenAI

# client = OpenAI()
from config import OPENAI_API_KEY, OPENAI_API_URL

client = OpenAI(api_key=OPENAI_API_KEY)



def parse_prompt(prompt: str):
    """
    Send a natural language prompt to GPT chat model to generate diagram structure.
    """
    response = client.chat.completions.create(model="gpt-4o",  # Ensure this is a valid chat model
    messages=[
        {"role": "system", "content": "You are an assistant that generates valid JSON for diagrams in Miro.Ensure the output includes an 'elements' list (nodes with labels and positions) and a 'connections' list (links between elements). Ensure the output is well-formed JSON. Return just the json object for the graph , no text before or after the json object."},
        {"role": "user", "content": prompt}
    ],
    
    temperature=0.4,response_format={"type":"json_object"})
    return response.choices[0].message.content.strip()

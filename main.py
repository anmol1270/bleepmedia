# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gpt_handler import parse_prompt
from miro import create_nodes_and_connections, ensure_board_exists

app = FastAPI()

class DiagramRequest(BaseModel):
    prompt: str
    board_name: str

import json  # Import the JSON module

@app.post("/generate-diagram/")
async def generate_diagram(request: DiagramRequest):
    """
    API endpoint to generate a diagram in Miro on the specified board.
    If the board does not exist, create it.
    """
    try:
        # Step 1: Ensure the board exists
        board_id = ensure_board_exists(request.board_name)
        print("board exists!!!!",board_id)

        # Step 2: Parse the user's prompt with GPT
        gpt_response = parse_prompt(request.prompt)
        print(gpt_response)
        print('gpt response got!!!!!')
        # Step 3: Safely parse the GPT response as JSON
        try:
            diagram_data = json.loads(gpt_response)
            
              # Use json.loads() instead of eval()
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON response from GPT: {e}")

        # Step 4: Generate the diagram on the board
        create_nodes_and_connections(diagram_data,board_id)
        return {"message": f"Diagram created successfully on board '{request.board_name}'!", "board_id": board_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

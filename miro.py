# miro.py
import requests
from config import MIRO_API_TOKEN

# MIRO_API_URL = f"https://api.miro.com/v2/boards/{MIRO_BOARD_ID}/widgets"


HEADERS = {
    "Authorization": f"Bearer {MIRO_API_TOKEN}",
    "Content-Type": "application/json"
}

def create_widget(data: dict,board_id):
    """
    Create a widget (node or connection) in Miro.
    """
    response = requests.post(f"https://api.miro.com/v2/boards/{board_id}/widgets", json=data, headers=HEADERS)
    return response.json()

def create_nodes_and_connections(diagram_data: dict,board_id):
    """
    Parse diagram data and create nodes and connections on Miro board.
    """
    # Create nodes
    node_ids = {}
    for element in diagram_data["elements"]:
        payload = {
            "type": "shape",
            "text": element["label"],
            "x": element.get("x", 0),
            "y": element.get("y", 0)
        }
        response = create_widget(payload,board_id)
        node_ids[element["id"]] = response["id"]

    # Create connections
    for connection in diagram_data["connections"]:
        payload = {
            "type": "connector",
            "startWidgetId": node_ids[connection["from"]],
            "endWidgetId": node_ids[connection["to"]]
        }
        create_widget(payload,board_id)


# miro.py
from config import MIRO_API_TOKEN

MIRO_BASE_URL = "https://api.miro.com/v2"
HEADERS = {
    "Authorization": f"Bearer {MIRO_API_TOKEN}",
    "Content-Type": "application/json"
}

def list_boards():
    """
    Retrieve the list of boards available in Miro.
    """
    response = requests.get(f"{MIRO_BASE_URL}/boards", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        response.raise_for_status()

def create_board(board_name: str):
    """
    Create a new board in Miro.
    """
    payload = {
        "name": board_name
    }
    response = requests.post(f"{MIRO_BASE_URL}/boards", json=payload, headers=HEADERS)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def ensure_board_exists(board_name: str):
    """
    Check if a board with the given name exists; if not, create it.
    Returns the board ID.
    """
    boards = list_boards()
    for board in boards:
        if board["name"] == board_name:
            return board["id"]

    # If board does not exist, create a new one
    new_board = create_board(board_name)
    return new_board["id"]

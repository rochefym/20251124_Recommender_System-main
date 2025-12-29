# Install websockets library if not already installed; Python 3.12 or lower is required
# command: pip install websockets

# Import the connect function from websockets library:
from websockets.sync.client import connect

# get_rag_response: Function to get response from RAG chain
def get_rag_response():
    # Sample question:
    question =  "A patient named Jackie Chan is a 76-year-old man. He is 175cms tall and weighs 71 kilos. He is having 320 grams of stir-fried seasonal vegetables and 220 grams of cabbage soup for his meal. Can you provide (1) an analysis, (2) suggestions, and (3) recommendations?"

    with connect("ws://120.117.116.47:25002") as websocket:
        #Send question to RAG chain server:
        message = question
        print(f"Send: {message}")
        websocket.send(message)

        #Receive response from RAG chain server:
        message = websocket.recv()
        print(f"Received: {message}")
        


# Function call to test the RAG response:
get_rag_response()

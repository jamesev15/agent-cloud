from fastapi import FastAPI
from pydantic import BaseModel
from agent import graph

app = FastAPI()

class MessageRequest(BaseModel):
    message: str

@app.post("/chatbot")
def chatbot(request: MessageRequest) -> dict:
    state = graph.invoke({"messages": [("user", request.message)]})
    return {"answer": state["messages"][-1].content}

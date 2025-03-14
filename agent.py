import logging
from typing import Annotated

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import os
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableLambda

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"] = "agent-cloud"


url = "https://e7f4684c-fd33-4db0-b1d3-268870ecb84d.europe-west3-0.gcp.cloud.qdrant.io:6333"
api_key = os.getenv("QDRANT_API_KEY")


COLLECTION_NAME = "idat-cloud"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def book_a_flight(flight_number: str, date: str):
    """Book a flight based on a flight number and for an specific date"""
    message = f"flight booked: {flight_number}/{date}"
    logger.info(message)
    return message

def search_flight_regulations(query: str):
    """Search information related to a query for an Airline called idat Airlines"""
    client = QdrantClient(
        url=url,
        api_key=api_key,
        https=True,
        timeout=300
    )

    vector_store_page = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002"),
    )
    retriever = vector_store_page.as_retriever()

    docs = retriever.invoke(query)

    return "\n\n".join(doc.page_content for doc in docs)

tools = [book_a_flight, search_flight_regulations]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()
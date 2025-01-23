from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os
from langfuse.decorators import observe
# Load environment variables
load_dotenv()

# Reference to existing SearchEngine class
from search_engine import SearchEngine

# Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    search_results: list

# Initialize components
search_engine = SearchEngine(
    csv_file="data/products.csv",
    exa_api_key=os.getenv("EXA_API_KEY")
)
llm = Ollama(model="mistral")

@observe(name="product_search")
def search_node(state: State):
    """Node that performs product search based on user query"""
    last_message = state["messages"][-1].content
    results = search_engine.search(last_message, top_k=5)
    return {"search_results": results}

@observe(name="chatbot")
def chatbot_node(state: State):
    """Node that generates response based on search results"""
    search_results = state.get("search_results", [])
    
    # Create a prompt that includes search results
    prompt = f"""You are a helpful shopping assistant. Based on the search results, help the user find the right product.
    Search Results: {search_results}
    
    Please format your response in a clear, concise way highlighting key product features and prices."""
    
    # Generate response using Mistral
    response = llm.invoke(prompt)
    
    # Return response as AIMessage
    return {"messages": [AIMessage(content=response)]}

# Build the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("search", search_node)
graph_builder.add_node("chatbot", chatbot_node)

# Add edges
graph_builder.add_edge("search", "chatbot")

# Set entry point
graph_builder.set_entry_point("search")

# Compile the graph
graph = graph_builder.compile() 
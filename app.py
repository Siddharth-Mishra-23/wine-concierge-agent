import os
from dotenv import load_dotenv
from typing import TypedDict, Dict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify, render_template
import json

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key or not os.getenv("TAVILY_API_KEY"):
    raise ValueError("GEMINI_API_KEY and TAVILY_API_KEY must be set in the .env file.")

# Initialize LLM and Tools
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=gemini_api_key
)
web_search_tool = TavilySearchResults(k=3)

# Define the custom weather tool
@tool
def get_weather(location: str):
    """
    Fetches the current weather for a given location.
    Provides dummy data for demonstration.
    """
    if "napa" in location.lower():
        return "The weather in Napa Valley is sunny with a temperature of 75°F. Perfect for a vineyard tour!"
    elif "london" in location.lower():
        return "It's a bit cloudy in London with a light drizzle. The temperature is 60°F."
    else:
        return f"Could not find weather data for {location}. Please specify a more well-known location."

# Define the RAG tool
try:
    loader = TextLoader("data/wine_info.txt")
    docs = loader.load()
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=gemini_api_key
    )
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()
    
    @tool
    def wine_info_retriever(query: str):
        """
        Retrieves information about the wine business from the provided document.
        Use this tool to answer questions about the business, its history,
        wines, or hours.
        """
        retrieved_docs = retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in retrieved_docs)
    
except FileNotFoundError:
    raise FileNotFoundError("data/wine_info.txt not found. Please create the file with content.")

# List of all tools available to the agent
tools = [web_search_tool, get_weather, wine_info_retriever]

# Define the system prompt for the agent
SYSTEM_PROMPT = """You are a helpful and knowledgeable conversational concierge for Vinetos de Sol winery.
Answer questions about the winery using the provided document.
For all other questions, use the search tools provided to find real-time information."""

# Build the agent using LangGraph's prebuilt utility
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("placeholder", "{messages}"),
        ]
    )
)

# Flask app setup
app_flask = Flask(__name__, static_folder='ui', template_folder='ui')

# Define the home page route to serve the UI
@app_flask.route('/')
def index():
    return render_template('index.html')

# Define the API endpoint for chat messages
@app_flask.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"response": "No message provided."}), 400

    inputs = {"messages": [HumanMessage(content=user_input)]}
    
    final_response_content = ""
    try:
        response = agent.invoke(inputs)
        final_message = response["messages"][-1]
        final_response_content = final_message.content
    except Exception as e:
        print(f"Error during agent invocation: {e}")
        final_response_content = "Sorry, an error occurred while processing your request."

    return jsonify({"response": final_response_content})

if __name__ == "__main__":
    print("Starting Flask web server...")
    app_flask.run(host='0.0.0.0', port=5000)
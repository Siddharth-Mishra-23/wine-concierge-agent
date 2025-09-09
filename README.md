Vinetos de Sol Conversational Concierge
Project Description
This project develops a smart conversational agent for a fictional wine business, Vinetos de Sol, in Napa Valley. Built with LangGraph and powered by Google's Gemini model, the agent serves as a "conversational concierge." It can answer questions from a private document about the business, perform real-time web searches, and provide updates like the weather. The project includes a basic, yet stylish, web-based chat UI built with Flask to provide a more engaging user experience.

Deliverables
Code: The complete source code is available in this GitHub repository.

README: This file provides a detailed overview, setup instructions, and a report on the project's development process.

Demo Video: A short (<1 min) demo video of the agent in action can be viewed here: [Insert a link to your demo video here, e.g., a YouTube link]

Approach
The conversational agent's logic is orchestrated using LangGraph, a powerful library for building stateful, multi-step agents. The core of the agent's intelligence is the Google Gemini 1.5 Flash model, which is configured to act as a reasoning engine.

The agent's capabilities are implemented as three distinct tools:

RAG Tool (wine_info_retriever): This tool handles questions about the wine business. It performs a Retrieval-Augmented Generation (RAG) search on the data/wine_info.txt file, which serves as the agent's internal knowledge base.

Web Search Tool (TavilySearchResults): This tool is used for general knowledge questions that require real-time information. It leverages the Tavily Search API for fast, relevant results.

Weather Tool (get_weather): A custom-built tool that provides dummy weather data for specific locations, demonstrating the agent's ability to fetch external, real-time information.

The user interface is a simple web application built with Flask, HTML, CSS, and JavaScript, which communicates with the LangGraph agent through a REST API endpoint.

Setup and Running the Project
Prerequisites
Python 3.10+

A Google Gemini API Key: Get one from Google AI Studio.

A Tavily API Key: Get one from Tavily.

Installation
Clone this repository:

Bash

git clone https://github.com/Siddharth-Mishra-23/wine-concierge-agent.git
cd wine-concierge-agent
Create and configure your .env file with your API keys. Do not commit this file.

GEMINI_API_KEY="your_gemini_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
Install the required Python packages:

Bash

pip install -r requirements.txt
Running the Application
Start the Flask web server from your terminal:

Bash

python app.py
A local server will start on port 5000. Open the provided URL in your browser to access the chat UI.

You can then ask questions to the agent to test its capabilities.

Challenges, Solutions, and Improvements
Challenges Encountered
API Quota and Authentication Errors: Initially, a RateLimitError was encountered with the OpenAI API.

Solution: The project was migrated to Google's Gemini API, which offers a free tier for development. This required updating the code and dependencies.

Gemini Credentialing Issues: The langchain-google-genai library produced DefaultCredentialsError and InvalidArgument errors due to strict requirements for API key formatting.

Solution: The problem was solved by explicitly passing the google_api_key to the LLM and embeddings constructors. The final code also switched to a more robust architecture using create_react_agent to handle tool-calling more reliably, eliminating persistent formatting errors.

UI Integration: The initial attempt to link the Flask backend with the HTML/CSS/JS files resulted in an unstyled UI due to incorrect file paths.

Solution: The Flask server was configured correctly, and the HTML file was updated to use the url_for('static', ...) helper function, ensuring the CSS and JavaScript files were served properly.

Possible Improvements
Add Conversational Memory: Implement langgraph.prebuilt.chat_agent_executor_with_tools to enable the agent to remember past conversations.

Real-time Weather API: Replace the dummy get_weather tool with a real weather API (e.g., OpenWeatherMap or AccuWeather) to provide live data.

Enhanced UI: Add features like typing indicators, streaming responses, and a more comprehensive mobile-responsive design.

User Authentication: Implement user authentication and store conversation history for a personalized experience.

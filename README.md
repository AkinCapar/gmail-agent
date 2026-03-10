# 📧 AI Gmail Assistant Agent

An intelligent, agentic email assistant built with **LangGraph**, **Streamlit**, and **OpenAI**. This agent securely connects to your Gmail account using the official Google API to read, draft, and send emails autonomously based on natural language commands.

## 🌟 Key Features

* **🧠 Agentic Workflow (ReAct):** The agent decides which tools to use dynamically. If you ask it to "Email John about the meeting," it knows to draft the content and invoke the send-email tool without rigid, hardcoded steps.
* **📬 Gmail API Integration:** Fully integrated with Google's official Python Client Library for secure, OAuth2-authenticated email management.
* **🛠️ Native Tool Calling:** Utilizes modern LLM tool-calling capabilities to translate user intent directly into actionable Python functions.
* **⚡ Interactive UI:** A clean, chat-based Streamlit interface that streams the agent's thought process and tool execution steps in real-time.

## 🏗️ Architecture

The system is orchestrated using a **LangGraph StateGraph**:
1.  **Agent Node:** The LLM (`gpt-5-mini`) processes the user prompt, determines the required action, and generates tool calls.
2.  **Tools Node:** Executes the specific Gmail operations (e.g., `send_email`, `read_recent_emails`) and feeds the observation back to the Agent.

*Note: Unlike full-memory conversational agents, this specific implementation is designed as a targeted task-execution agent, focusing on immediate email operations per session without retaining long-term cross-session memory.*

## 🛠️ Tech Stack

* **Framework:**  LangChain/LangGraph
* **LLM:** OpenAI (`gpt-5-mini`)
* **UI:** Streamlit
* **API:** Google Workspace (Gmail API)


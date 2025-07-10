from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from rag import get_context, store_conversation
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

class ConversationState:
    def __init__(self):
        self.history = []
        self.intent = None

async def detect_intent(query: str) -> str:
    # Simple intent detection (extend with NLP for production)
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in ["price", "cost", "buy", "purchase"]):
        return "sales"
    elif any(keyword in query_lower for keyword in ["help", "support", "issue", "problem"]):
        return "support"
    return "unknown"

async def llm_node(state: ConversationState, query: str) -> str:
    try:
        state.intent = await detect_intent(query)
        context = await get_context(query)

        if state.intent == "sales":
            prompt = [
                SystemMessage(content="You are a sales agent. Provide concise product information and pricing."),
                HumanMessage(content=f"Context: {context}\nUser: {query}")
            ]
        elif state.intent == "support":
            prompt = [
                SystemMessage(content="You are a support agent. Provide helpful troubleshooting or escalate if needed."),
                HumanMessage(content=f"Context: {context}\nUser: {query}")
            ]
        else:
            prompt = [
                SystemMessage(content="You are a helpful voice AI agent. Answer clearly and concisely."),
                HumanMessage(content=f"Context: {context}\nUser: {query}")
            ]

        state.history.append(query)
        response = await llm.invoke(prompt)
        state.history.append(response.content)

        # Store conversation in ChromaDB
        await store_conversation(query, state.intent)
        return response.content
    except Exception as e:
        print(f"Error in llm_node: {e}")
        return {"llm": "Sorry, I encountered an error. Please try again."}

def create_graph():
    graph = StateGraph(ConversationState)
    graph.add_node("llm", llm_node)
    graph.set_entry_point("llm")
    graph.add_edge("llm", END)
    return graph.compile()

async def handle_conversation(query: str) -> str:
    graph = create_graph()
    state = ConversationState()
    result = await graph.invoke({"query": query, "state": state})
    return result["llm"]
from langchain.agents import tool, AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from document_qa import setup_document_qa
from appointment import AppointmentSystem
from typing import Optional, List
import os
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self, document_path: str):
        self.document_qa = setup_document_qa(document_path)
        self.appointment_system = AppointmentSystem()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Define tools using bound methods
        self.tools = [
            self._create_document_qa_tool(),
            self._create_appointment_tool()
        ]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant. Use tools when appropriate:
            - document_qa_tool: For questions about documents
            - schedule_appointment_tool: For booking appointments"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _create_document_qa_tool(self):
        @tool
        def document_qa_tool(query: str) -> str:
            """Answers questions about document content."""
            return self.document_qa.invoke({"input": query})["answer"]
        return document_qa_tool
    
    def _create_appointment_tool(self):
        @tool
        def schedule_appointment_tool(query: str) -> str:
            """Handles appointment scheduling."""
            response = self.appointment_system.collect_info(query)
            if response["status"] == "complete":
                valid, result = self.appointment_system.validate_and_confirm()
                if valid:
                    confirmation = (
                        f"✅ Appointment confirmed for {result.appointment_date}\n"
                        f"📞 Contact: {result.phone}\n"
                        f"📧 Email: {result.email}"
                    )
                    self.appointment_system.reset()
                    return confirmation
                return f"❌ Error: {result}"
            return response["message"]
        return schedule_appointment_tool
    
    def chat(self, query: str, history: Optional[List] = None) -> str:
        if history is None:
            history = []
        
        result = self.agent_executor.invoke({
            "input": query,
            "chat_history": history
        })
        return result["output"]
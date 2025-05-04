from chatbot import Chatbot
import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage

def main():
    load_dotenv()
    
    # Initialize with path to your document
    bot = Chatbot("data/documents/doc.pdf")
    
    print("Chatbot initialized. Type 'exit' or 'quit' to end the session.")
    print("You can ask about the document or request an appointment.")
    
    chat_history = []
    while True:
        query = input("\nYou: ")
        if query.lower() in ['exit', 'quit']:
            break
        response = bot.chat(query, chat_history)
        print(f"Bot: {response}")
        chat_history.extend([
            HumanMessage(content=query),
            AIMessage(content=response)
        ])

if __name__ == "__main__":
    main()
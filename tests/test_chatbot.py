import pytest
from app.chatbot import Chatbot
from unittest.mock import patch

@pytest.fixture
def mock_chatbot():
    with patch('app.document_qa.setup_document_qa'), \
         patch('app.chatbot.ChatGoogleGenerativeAI'):
        yield Chatbot("dummy_path.pdf")

def test_chatbot_initialization(mock_chatbot):
    assert mock_chatbot is not None

def test_document_qa_tool(mock_chatbot):
    mock_chatbot.document_qa.invoke.return_value = {"answer": "Test answer"}
    response = mock_chatbot.document_qa_tool("test query")
    assert response == "Test answer"
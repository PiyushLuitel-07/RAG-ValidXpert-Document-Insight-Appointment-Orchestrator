# Document Intelligence & Appointment Chatbot

<div align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-0.1.0-orange" alt="LangChain">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</div>

## Project Overview
A sophisticated AI assistant combining:
- **Document Intelligence**: Answer questions from PDFs/websites using RAG
- **Appointment Scheduling**: Natural language booking system
- **Data Validation**: Automatic verification of user inputs

## Features

### 📚 **Document Intelligence**
| Feature | Description | Example |
|---------|-------------|---------|
| **Multi-Format Support** | Process PDFs & web URLs | `policy.pdf`, `https://docs.example.com` |
| **Semantic Search** | Find answers using meaning, not just keywords | _"What's the late fee policy?"_ → Shows exact clause |
<!-- | **Citation Tracking** | Identify source pages/sections | _"From page 12 of the policy..."_ | -->

### 📅 **Appointment Management**
| Feature | Description | Tech Used |
|---------|-------------|-----------|
| **Natural Language Dates** | Understand casual time references | `"next Tuesday at 3"` → `2024-06-18 15:00` |
| **Multi-Step Booking** | Guided info collection | Name → Phone → Email → Confirm |
<!-- | **Calendar Sync** | (Coming Soon) | Google Calendar API | -->

### 🛡️ **Data Validation**
```python
# Example validation rules
class UserInfo(BaseModel):
    name: str
    phone: str
    email: EmailStr   # A emailstr datatype provided by Pydantic
    appointment_date: datetime
    
    @validator('phone')
    def validate_phone(cls, v):
        v = ''.join(filter(str.isdigit, v))  # Remove any non-digit characters
        if len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v
    
    @validator('appointment_date')
    def validate_future_date(cls, v):
        if v < datetime.now():
            raise ValueError("Appointment date must be in the future")
        return v
```

## Project File Structure

```bash
.
├── app/                   # Main application code
│   ├── main.py            # Entry point for the chatbot application
│   ├── chatbot.py         # Core chatbot logic and agent setup
│   ├── document_qa.py     # Document question-answering system
│   ├── appointment.py     # Appointment scheduling functionality
│   └── models.py          # Data models and validation schemas
│
├── data/                  # Data storage
│   └── documents/         # Directory for PDF/document storage
│       └── policy.pdf     # Example document (add your files here)
│
├── tests/                 # Test cases
│   ├── test_chatbot.py    # Unit tests for chatbot functionality
# │   ├── test_document_qa.py # Document QA system tests
# │   └── test_appointment.py # Appointment system tests
│
├── .env                   # Environment variables
│   # Example contents:
│   # GOOGLE_API_KEY=api_key_here
│   # DOCUMENT_PATH=data/documents/doc.pdf
│
└── requirements.txt       # Python dependencies
│   # Core requirements:
│   # langchain
│   # langchain-google-genai
│   # python-dotenv
│   # pydantic
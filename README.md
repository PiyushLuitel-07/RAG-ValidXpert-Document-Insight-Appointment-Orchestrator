# Document Intelligence & Appointment Chatbot

<div align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-0.1.0-orange" alt="LangChain">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</div>

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technical Architecture](#technical-architecture)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [Usage Examples](#usage-examples)
7. [Core Components](#core-components)
8. [Troubleshooting](#troubleshooting)
9. [Roadmap](#roadmap)


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
| **Citation Tracking** | Identify source pages/sections | _"From page 12 of the policy..."_ |

### 📅 **Appointment Management**
| Feature | Description | Tech Used |
|---------|-------------|-----------|
| **Natural Language Dates** | Understand casual time references | `"next Tuesday at 3"` → `2024-06-18 15:00` |
| **Multi-Step Booking** | Guided info collection | Name → Phone → Email → Confirm |
| **Calendar Sync** | (Coming Soon) | Google Calendar API |

### 🛡️ **Data Validation**
```python
# Example validation rules
class UserInfo(BaseModel):
    email: EmailStr
    phone: constr(regex=r"^\d{10}$")  # 10 digits
    date: datetime = Field(gt=datetime.now())  # Future dates
```

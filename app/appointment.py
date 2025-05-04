from datetime import datetime
from dateutil import parser
from typing import Optional, Dict, Any, Tuple
from models import UserInfo
import re

class AppointmentSystem:
    def __init__(self):
        self.current_data: Dict[str, Any] = {}
    
    def extract_date(self, text: str) -> Optional[datetime]:
        try:
            # First clean the input string
            clean_text = re.sub(r'[^\w\s:-]', '', text.strip())
            
            # Parse with strict bounds checking
            parsed_date = parser.parse(clean_text, fuzzy=True)
            
            # Validate date range (1900-2100)
            if parsed_date.year < 1900 or parsed_date.year > 2100:
                return None
                
            return parsed_date
        except (ValueError, TypeError, OverflowError):
            return None
    
    def collect_info(self, user_input: str) -> Dict[str, str]:
        try:
            # Step 1: Extract date if not already collected
            if not self.current_data.get("appointment_date"):
                date = self.extract_date(user_input)
                if date:
                    self.current_data["appointment_date"] = date
                    return {
                        "status": "date_received", 
                        "message": "Great! What's your full name?"
                    }
            
            # Step 2: Collect name
            if not self.current_data.get("name"):
                self.current_data["name"] = user_input
                return {
                    "status": "name_received", 
                    "message": "Thanks! What's your phone number?"
                }
            
            # Step 3: Collect phone
            if not self.current_data.get("phone"):
                self.current_data["phone"] = user_input
                return {
                    "status": "phone_received", 
                    "message": "Finally, what's your email address?"
                }
            
            # Step 4: Collect email
            if not self.current_data.get("email"):
                self.current_data["email"] = user_input
                return {
                    "status": "complete", 
                    "message": "Validating your information..."
                }
            
            return {"status": "complete", "message": "Ready to confirm!"}
        except Exception as e:
            return {"status": "error", "message": f"Error: {str(e)}"}
    
    def validate_and_confirm(self) -> Tuple[bool, Any]:
        try:
            user_info = UserInfo(**self.current_data)
            return True, user_info
        except Exception as e:
            return False, str(e)
    
    def reset(self):
        self.current_data = {}
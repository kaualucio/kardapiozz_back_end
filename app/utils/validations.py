from re import match

def is_email_valid(email: str) -> bool:
  email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  
  if not match(email_regex, email.strip()):
    return False
    
  return True
  
def is_password_valid(password: str) -> bool:
  password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$'
    
  if match(password_regex, password.strip()):
      return True
  else:
      return False
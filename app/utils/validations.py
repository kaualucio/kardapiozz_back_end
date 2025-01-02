from re import match, sub

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
    
def is_phone_valid(phone_number: str) -> bool:
  # Remove espaços, parênteses e traços
  phone_number = sub(r'[()\s-]', '', phone_number)

  # Regex para validar telefone brasileiro
  pattern = r'^\d{2}9\d{8}$|^\d{2}\d{8}$'
  
  # Verifica se o telefone corresponde ao padrão
  if match(pattern, phone_number):
      return True
  return False

def normalize_phone_number(phone: str) -> str:
  # Remove espaços, parênteses e traços
  phone_number = sub(r'[()\s-]', '', phone)
  
  return phone_number
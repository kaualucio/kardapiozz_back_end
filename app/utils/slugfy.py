from re import sub

def slugfy(text: str) -> str:
  text = text.lower()
  text = sub(r'[\s]+', '-', text)  
  text = sub(r'[^\w\-]', '', text)  
  text = sub(r'--+', '-', text)     
  text = text.strip('-')               
  return text
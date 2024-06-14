import os
import google.generativeai as genai
import requests
import fitz 
from datetime import datetime

def get_models():
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)

def generate_content():
  generate_content('hell,what is diff from gemini-1.5-pro gemini-1.5-flase')

def generate_content_with_prompt(prompt,content):
  if content is None:
    print("content is None")
    return
  tmp = prompt + content
  generate_content(tmp)

def generate_content(content):
  if content is None:
    print("content is None")
    return
  model_name = os.getenv("MODEL_NAME",'gemini-1.5-flash')
  model = genai.GenerativeModel(model_name)
  response = model.generate_content(content)
  print(response.text)

def download_pdf(url,filename):
  response = requests.get(url)
  if response.status_code == 200:
      with open(filename, "wb") as f:
          f.write(response.content)
      print("PDF downloaded successfully.")
  else:
      print(f"Failed to retrieve the PDF. Status code: {response.status_code}")

  
def get_pfd_text(pdf_path):
  if (pdf_path is None or os.path.exists(pdf_path) == False ):
    print(f"{pdf_path} is None")
    return
  document = fitz.open(pdf_path)
  all_text = ""

  for page_num in range(len(document)):
      page = document.load_page(page_num)
      all_text += page.get_text()
  return all_text

prompt = os.getenv('PROMPT')
print(f"prompt = {prompt}")


today =  datetime.today()
today_str = os.getenv("SPRCIAL_DATE",today.strftime('%Y%m%d'))

url = os.getenv("URL")
items = os.getenv("FILES").split(",")
for item in items:
  full_path= f"{url}{item}{today_str}.pdf"
  print(f"download {full_path}")

  filename = f"{item}.pdf"
  download_pdf(full_path,filename)
  pdf_context = get_pfd_text(filename)
  generate_content_with_prompt(prompt=prompt,content=pdf_context)
import os
import google.generativeai as genai
import requests
import fitz 
from datetime import datetime, timedelta
from dotenv import load_dotenv

def get_models():
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)

def generate_content():
  return generate_content('hell,what is diff from gemini-1.5-pro gemini-1.5-flase')

def generate_content_with_prompt(prompt,content):
  if content is None:
    print("content is None")
    return
  tmp = prompt + content
  return generate_content(tmp)

def generate_content(content):
  if content is None:
    print("content is None")
    return
  model_name = os.getenv("MODEL_NAME",'gemini-1.5-flash')
  model = genai.GenerativeModel(model_name)
  response = model.generate_content(content)
  return response.text

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

def append_to_file(filename,content):
  with open(filename, "a") as file:
    # Write the content to the file
    file.write(content + "\n")



load_dotenv("./conf/.env") 

prompt = os.getenv('US_PROMPT')
print(f"prompt = {prompt}")

today  = datetime.today()
yesterday = today - timedelta(days=1)
today_str = os.getenv("US_SPRCIAL_DATE",yesterday.strftime('%Y%m%d'))

save_file = os.getenv("SAVE_FILE")
url = os.getenv("US_URL")

items = os.getenv("US_FILES").split(",")
for item in items:
  full_path= f"{url}{item}{today_str}.pdf"
  print(f"download {full_path}")

  filename = f"{item}.pdf"
  download_pdf(full_path,filename)
  pdf_context = get_pfd_text(filename)
  gen_content = generate_content_with_prompt(prompt=prompt,content=pdf_context)
  
  save_contrent = f"*****{today_str}{filename} ***** \n {gen_content} \n *****{today_str}***** \n "
  append_to_file(save_file,save_contrent)
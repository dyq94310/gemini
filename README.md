download PDF files and extract text from them using Python.
extract text to Gemini and get text from Gemini save as file

.env
```
GOOGLE_API_KEY=
MODEL_NAME=
US_PROMPT="tell me federalreserve say,give me conclusions and recommendations but Need to be professional, detailed, and not give misleading information. Answer me use chiness. the content is:  \n "
US_FILES=""
US_URL="https://www.federalreserve.gov/monetarypolicy/files/"
# US_SPRCIAL_DATE=20240501
SAVE_FILE=./data/CONTEXT.data
```

user venv
```
python -m venv .
```

install requirements
```
pip install python-dotenv
pip install PyMuPDF
pip install requests
pip install -q -U google-generativeai
```

```
pip freeze > requirements.txt
```
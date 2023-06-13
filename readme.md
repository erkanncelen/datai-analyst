**DATAI ANALYST**

DatAI Analyst enables you to query an example database using natural language.

Steps to run locally:

1. Create .env file with:
ENDPOINT = {openai endpoint here}
DEPLOYMENT-NAME = {gpt deployment name here}
API-KEY = {openai api key here}

2. install requirements:
pip install -r requirements.txt

3. run ingest.py once:
python ingest.py

4. run flask app at http://127.0.0.1:8001 address:
flask --app app run --port=8001

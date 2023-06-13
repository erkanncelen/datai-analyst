from flask import Flask, render_template, request
from functions import gpt_query

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/', methods=['POST'])
def query_button():
   question = request.form['question']
   if question == "Who is the best AE ever?":
      result = "<h1>Erkan!\n:)))))</h1>"
   else:
      result = gpt_query(question=question)
   return render_template('index.html', result = result, question=question)

if __name__ == '__main__':
   app.run(debug=True, port=8001)

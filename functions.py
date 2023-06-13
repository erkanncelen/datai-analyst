import openai
import time
import os
import duckdb
import pandas
import time
from pretty_html_table import build_table
from dotenv import load_dotenv

load_dotenv()
deployment_name = os.getenv("DEPLOYMENT-NAME")
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = os.getenv("ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("API-KEY")

def gpt_communicator(text: str = None, question: str = None, verbose=True, query:str=None, error_message:str=None, give_reasoning:bool=False):
    if give_reasoning:
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
            messages=[
                {
                    "role": "user",
                    "content": f"""
        \"{text}\"

        I asked you to give me an executable SQL query that would answer the question below, based on the schema above.

        Question: {question}

        You then gave me the following query.
        
        Query: {query}

        I tried running your query but the database gave me the following error.
        
        Error: {error_message}

        We are a company and we wonder why we cannot answer the question above using the data we have.
        Can you please give an explaination why this failed and what we may need to do in order to be able to answer the question above?
        Please give us your recommendations. You can tell what is missing, what can be improved, or what we can do differently.
        Keep it short, no more than 100 words long.
        """,
                }
            ],
        )
        reasoning = response["choices"][0]["message"]["content"]
        return reasoning
    
    elif not error_message:
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
            messages=[
                {
                    "role": "user",
                    "content": f"""
        \"{text}\"

        Based on the schema above, give me an executable SQL query that would answer the question below, in PostgreSQL dialect.
        Make sure to write column and table names exactly as they are written in the schema above.
        Give me only the SQL query text.
        
        Question: {question}
        """,
                }
            ],
        )

        answer = response["choices"][0]["message"]["content"]
        if verbose:
            print
            print(text)
            print(question)
            print("\n")
            print(f"===> {answer}")
            print("----------------\n")
        return answer
    if error_message:
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
            messages=[
                {
                    "role": "user",
                    "content": f"""
        \"{text}\"

        I asked you to give me an executable SQL query that would answer the question below, based on the schema above.

        Question: {question}

        You then gave me the following query.
        
        Query: {query}

        I tried running your query but the database gave me the following error.
        
        Error: {error_message}

        Can you please fix your query so that it will run without an error this time?
        Make sure to write column and table names exactly as they are written in the schema.
        Don't apologise, don't say things like 'I apologize for the mistake in my previous response.'. 
        Give me only the SQL query text, in PostgreSQL dialect. RETURN NOTHING ELSE THAN THE SQL CODE ITSELF!
        """,
                }
            ],
        )

        answer = response["choices"][0]["message"]["content"]
        if verbose:
            print(f"""
        \"{text}\"

        I asked you to give me an executable SQL query that would answer the question below, based on the schema above.

        Question: {question}

        You then gave me the following query.
        
        Query: {query}

        I tried running your query but the database gave me the following error.
        
        Error: {error_message}

        Can you please fix your query so that it will run without an error this time?
        Make sure to write column and table names exactly as they are written in the schema.
        Don't apologise, don't say things like 'I apologize for the mistake in my previous response.'. 
        Give me only the SQL query text, in PostgreSQL dialect. RETURN NOTHING ELSE THAN THE SQL CODE ITSELF!
        """)
            # print(f"question: {question}")
            # print(f"query: {query}")
            # print(f"error_message: {error_message}")
            print("\n")
            print(f"===> {answer}")
            print("----------------\n")
        return answer

def gpt_query(question:str=None):

    con = duckdb.connect('warehouse.db')
    tables = ["dim_city", "dim_customer", "dim_date", "dim_employee", "dim_stock_item", "fact_sales"]
    text = ""
    for table_name in tables:
        schema = f"table name: {table_name}" + "\n" + str(con.sql(f"DESCRIBE {table_name}"))
        text += "\n\n" + schema

    query = gpt_communicator(text=text,question=question,verbose=True)
    try:
        result_df = con.sql(f"{query}").df()
        result_html = build_table(result_df, color='grey_light', font_size='medium', font_family='Helvetica, sans-serif', text_align='left')
        return result_html
    except Exception as e:
        try:
            time.sleep(2)
            error_message = e
            query = gpt_communicator(text=text, question=question, verbose=True, query=query, error_message=error_message)
            result_df = con.sql(f"{query}").df()
            result_html = build_table(result_df, color='grey_light', font_size='medium', font_family='Helvetica, sans-serif', text_align='left')
            return result_html
        except Exception as e:
            try:
                time.sleep(2)
                error_message = e
                reasoning = gpt_communicator(text=text, question=question, verbose=True, query=query, error_message=error_message, give_reasoning=True)
                return reasoning
            except:
                return "I'm sorry, I can't write a query that answers your question."

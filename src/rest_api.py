from flask import Flask
import duckdb_llamba_index as dli

app = Flask(__name__)


@app.get('/query/<question>')
def find_answers(question):
    return dli.get_answer(question)

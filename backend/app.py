from flask import Flask, request, jsonify
import os
from openai import OpenAI, RateLimitError
from prompt import get_sql_prompt
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_sql_local(prompt):
    payload = {
        "model": "llama3",
        "prompt": f"""
        You are an expert SQL generator.
        Convert the following natural language request into a valid MySQL query.
        Return only SQL query.

        User Request: {prompt}
        SQL:
        """,
                "stream": False
            }

    response = requests.post(OLLAMA_URL, json=payload)
    data = response.json()
    return data["response"].strip()

@app.route("/generate-sql", methods=["POST"])
def generate_sql():
    try:
        data = request.json
        user_query = data.get("query")

        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        sql_query = generate_sql_local(user_query)

        return jsonify({"sql": sql_query})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to generate SQL"}), 500

if __name__ == "__main__":
    app.run(debug=True)
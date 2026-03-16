from flask import Flask, request, jsonify, Blueprint
import os
from openai import OpenAI, RateLimitError
from core.controller.prompt import get_sql_prompt
from core.model.BOModel import BOModel
from flask_cors import CORS
import requests
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from transformers import MarianMTModel, MarianTokenizer
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Blueprint('BO', __name__)



# Import from your local file
try:
    from image_generator import text_to_image, text_to_image_base64, get_generator
    print("✅ Successfully imported image_generator")
except ImportError as e:
    print(f"❌ Failed to import image_generator: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    sys.exit(1)

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



# @app.route("/generate-sql", methods=["POST"])
def generate_sql():
    try:
        data = request.json
        user_query = data.get("query")

        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        sql_query = generate_sql_local(user_query)
        # sql_query = generate_image(user_query)
            
        return jsonify({"sql": sql_query})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to generate SQL"}), 500

@app.route("/generate-sql", methods=["POST"])
def generate_image():
    """Generate image from text prompt"""
    try:
        data = request.json
        prompt = data.get("query")
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        print(f"Generating image for: {prompt}")
        
        # Generate image and get base64
        image_base64 = text_to_image_base64(
            prompt,
            num_inference_steps=30,
            save=True
        )
        
        return jsonify({
            "success": True,
            "image": image_base64,
            "prompt": prompt
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('api/get/all_users',methods=['POST','GET'])
def GetAllUsers():
    try:
        get_users=BOModel().GetAllUser()
        # print(get_users)
        if get_users:
            return jsonify({
                "success": True,
                "data": get_users
            }), 200
        else:
            return jsonify({"success":False,"error":"No data"}),500
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500 
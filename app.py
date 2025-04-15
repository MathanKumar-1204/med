from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY environment variable is required")

# Configure Generative AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    chat = model.start_chat(history=[])
    logger.info("Successfully configured Generative AI")
except Exception as e:
    logger.error(f"Failed to configure Generative AI: {str(e)}")
    raise

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    try:
        user_message = request.form.get("message", "").strip()
        
        logger.debug(f"Received message: {user_message}")

        if not user_message:
            return jsonify({"error": "Message cannot be empty."}), 400

        try:
            response = chat.send_message(user_message)
            response_text = response.text
            logger.debug("Successfully got response from model")
            return jsonify({"response": response_text})
        except Exception as e:
            logger.error(f"Error getting response from model: {str(e)}")
            return jsonify({"error": f"Error getting response from model: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Unexpected error in chat_route: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

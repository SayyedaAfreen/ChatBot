from flask import Flask, render_template, request, jsonify 
import os 
import google.generativeai as genai 
from dotenv import load_dotenv 

load_dotenv()  # Load environment variables 
 
app = Flask(__name__) 
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 
 
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[]) 
 
def get_gemini_response(question): 
    response = chat.send_message(question, stream=True) 
    response_message = " ".join([chunk.text for chunk in response]) 
    return response_message 
 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/get_response', methods=['POST']) 
def get_response(): 
    user_message = request.json.get('message') 
    print(f"Received message: {user_message}") 
    if not user_message: 
        return jsonify({"response": "Error: No message provided."}) 


    response_message = get_gemini_response(user_message) 
    print(f"Response message: {response_message}") 
    return jsonify({"response": response_message}) 

if __name__ == '__main__': 
    app.run(debug=True)  
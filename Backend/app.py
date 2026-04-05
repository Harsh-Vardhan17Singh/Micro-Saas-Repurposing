from flask import Flask,request,jsonify
from services.ai_service import generate_content
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello! Backend Is Running"

@app.route("/generate",methods =['POST'])
def generate():
    # 1.Get Text
    data = request.get_json()

    # 2. Validate
    if not data or "text" not in data:
        return jsonify({
            "error":"Invalid Input"
        })
    
    text = data.get("text")

    tone = data.get("tone","professional")
    
    
    #2.Print Data
    print("Received text",text)

    #3.get Dummy data
    ai_output = generate_content(text,tone)

    # 4.return jsonify
    
    return jsonify (ai_output)
    
    




if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask,request,jsonify
from services.ai_service import generate_content
from flask_cors import CORS

user_usage = {}
FREE_LIMIT = 3


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello! Backend Is Running"

@app.route("/generate",methods =['POST'])
def generate():
    # 1.Get Text
    data = request.get_json()

    # Validate first
    if not data or "text" not in data:
        return jsonify({
            "error":"Invalid Input"
        }) 

    user_id = data.get("userId",'anonymous')

    if user_id not in user_usage:
        user_usage[user_id] = 0
    if user_usage[user_id] >= FREE_LIMIT:
        return jsonify({
            "error":"limit_reached",
            "message":"Free limit reached"
        })

    # 2. Validate
    if not data or "text" not in data:
        return jsonify({
            "error":"Invalid Input"
        })
    
    text = data.get("text")

    tone = data.get("tone","professional")

    format = data.get("format","social")
    
    
    #2.Print Data
    print(f"[{user_id}] Usage: {user_usage[user_id]}/{FREE_LIMIT}")

    #3.get Dummy data
    ai_output = generate_content(text,tone,format)

    # Only Count if no error
    if isinstance(ai_output,dict) and "error" not in ai_output:
        user_usage[user_id] += 1 

    

    # 4.return jsonify
    
    return jsonify ({
        **ai_output,
        "usage":user_usage[user_id],
        "limit":FREE_LIMIT
    })
    
    




if __name__ == "__main__":
    app.run(debug=True)
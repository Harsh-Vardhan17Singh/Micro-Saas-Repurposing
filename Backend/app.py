from flask import Flask,request,jsonify
from services.ai_service import generate_content
from flask_cors import CORS
from database import init_db, get_user, create_user,update_usage

app = Flask(__name__)
CORS(app)

FREE_LIMIT = 100 

@app.route("/")
def home():
    return "Hello! Backend Is Running"

@app.route("/generate",methods =['POST'])
def generate():
    # 1.Get Text
    data = request.get_json(silent = True)

    # Validate first
    if not data or "text" not in data:
        return jsonify({
            "error":"Invalid Input"
        }),400
    
    if len(data.get("text","")) > 5000:
        return jsonify({"error":"Text too long"}),400


    user_id = data.get("userId",'anonymous')
    ip = request.remote_addr

    #bind user with IP
    user_id = f"{user_id}_{ip}"

    # Get User From Database
    user = get_user(user_id)

    if not user:
        create_user(user_id)
        usage = 0
        plan = "free"
    else:
        usage,plan = user
    
    # CHECK LIMIT
    if plan == "free" and usage >= FREE_LIMIT:
        return jsonify({
            "error":"limit_reached",
            "message":"Free limit reached"
        })
    
    text = data.get("text")

    tone = data.get("tone","professional")

    format = data.get("format","social")
    
    
    #2.Print Data
    print(f"[REQUEST] user ={user_id} Usage: {usage}/{FREE_LIMIT}")

    #3. AI CALL
    try:
     ai_output = generate_content(text,tone,format)
    except Exception as e:
     print("AI ERROR:",str(e))
     return jsonify({"error":"AI service failed"}),500

    # Update Usage Only If Success
    if isinstance(ai_output,dict) and "error" not in ai_output:
        usage += 1
        update_usage(user_id,usage) 

    

    # 4.return jsonify
    
    return jsonify ({
        **ai_output,
        "usage":usage,
        "limit":FREE_LIMIT
    })
    
    




if __name__ == "__main__":
    init_db()
    app.run()
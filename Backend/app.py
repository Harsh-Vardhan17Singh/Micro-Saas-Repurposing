from flask import Flask,request,jsonify
from services.ai_service import generate_content



app = Flask(__name__)

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
    
    
    #2.Print Data
    print("Received text",text)

    #3.get Dummy data
    ai_output = generate_content(text)

    # 4.return jsonify
    
    return jsonify({
        "twitter":ai_output,
        "linkedin":ai_output,
        "summary":ai_output
    
    }) 
    
    




if __name__ == "__main__":
    app.run(debug=True)
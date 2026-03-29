from flask import Flask,request,jsonify



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
    response = (f"Your text:{text}")

    # 4.return jsonify
    
    return jsonify({
        "twitter":response,
        "linkedin":response,
        "summary":response
    
    }) 
    
    




if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
import google.generativeai as genai


app = Flask(__name__)

# Configurar a API Key do Gemini

genai.configure(api_key="AIzaSyAHgqh_lbkITO8zS5F0cMckHH2ihXhhVZM")

@app.route("/gemini", methods=["POST"])
def chat():
    data = request.json
    pergunta = data.get("pergunta", "")

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(pergunta)

    return jsonify({"resposta": response.text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

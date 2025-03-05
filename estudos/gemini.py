import google.generativeai as genai

# Configurar a API Key
genai.configure(api_key="AIzaSyAHgqh_lbkITO8zS5F0cMckHH2ihXhhVZM")

# Escolher o modelo Gemini
model = genai.GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Escreva um código Python para converter um arquivo CSV em JSON.")

print(response.text)

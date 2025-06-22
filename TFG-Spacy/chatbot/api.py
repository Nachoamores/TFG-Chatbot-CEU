from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import spacy
import re
import unicodedata

app = Flask(__name__)
CORS(app)

# Cargar modelo NLP en español
nlp = spacy.load("es_core_news_md")

# Cargar el archivo JSON de preguntas
def cargar_faq(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

faqs = cargar_faq("faq_data.json")

# Función normalización
def normalizar_pregunta(texto):
    if not texto:
        return ""

    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join([c for c in texto if unicodedata.category(c) != 'Mn'])
    texto = re.sub(r"http[s]?://\S+", "", texto)
    texto = re.sub(r"[¿?¡!.,]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto

# Buscar la pregunta más parecida por significado
def encontrar_respuesta(pregunta_usuario, faqs, umbral=0.75):
    pregunta_normalizada = normalizar_pregunta(pregunta_usuario)
    doc_usuario = nlp(pregunta_normalizada)

    mejor_similitud = 0
    respuesta_encontrada = None
    pregunta_match = ""

    for item in faqs:
        lista_preguntas = [item["pregunta"]] + item.get("reformulaciones", [])
        for pregunta in lista_preguntas:
            doc_pregunta = nlp(normalizar_pregunta(pregunta))
            similitud = doc_usuario.similarity(doc_pregunta)

            if similitud > mejor_similitud:
                mejor_similitud = similitud
                respuesta_encontrada = item["respuesta"]
                pregunta_match = pregunta

    # Mostrar logs para depurar
    print("🟡 Pregunta del usuario:", pregunta_usuario)
    print("🟢 Coincidencia encontrada:", pregunta_match)
    print(f"📊 Similitud: {mejor_similitud:.4f}")

    # Fallback adaptativo
    if mejor_similitud >= umbral:
        return respuesta_encontrada
    elif mejor_similitud >= 0.5:
        return f"No estoy completamente seguro, pero puede que te refieras a esto:\n\n{respuesta_encontrada}"
    else:
        return "Lo siento, no tengo una respuesta clara para eso. Intenta reformular tu pregunta o sé más específico."

# Ruta de la API
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    pregunta = data.get("pregunta", "")
    respuesta = encontrar_respuesta(pregunta, faqs)
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(port=5000)

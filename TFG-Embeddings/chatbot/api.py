from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import unicodedata
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

app = Flask(__name__)
CORS(app)

# Cargar modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Cargar JSON de preguntas
def cargar_faq(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

faqs = cargar_faq("faq_data.json")

# Función mejorada de normalización
def normalizar_pregunta(texto):
    if not texto:
        return ""

    texto = texto.lower().strip()

    # Eliminar tildes 
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join([c for c in texto if unicodedata.category(c) != 'Mn'])

    # Eliminar URLs
    texto = re.sub(r"http[s]?://\S+", "", texto)

    # Eliminar puntuación común
    texto = re.sub(r"[¿?¡!.,]", "", texto)

    # Eliminar espacios redundantes
    texto = re.sub(r"\s+", " ", texto)

    return texto

# Preparar preguntas y respuestas
preguntas_totales = []
respuestas_totales = []

for item in faqs:
    frases = [item["pregunta"]] + item.get("reformulaciones", [])
    for f in frases:
        preguntas_totales.append(normalizar_pregunta(f))
        respuestas_totales.append(item["respuesta"])

# Configurar ChromaDB
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="faq", embedding_function=embedding_func)

# Añadir datos al vector store
for i, pregunta in enumerate(preguntas_totales):
    collection.add(
        documents=[pregunta],
        metadatas=[{"respuesta": respuestas_totales[i]}],
        ids=[str(i)]
    )

# Buscar mejor respuesta
def encontrar_respuesta(pregunta_usuario, umbral=0.65):
    pregunta_normalizada = normalizar_pregunta(pregunta_usuario)
    resultados = collection.query(
        query_texts=[pregunta_normalizada],
        n_results=1
    )

    resultado = resultados["metadatas"][0][0]
    similitud = resultados["distances"][0][0]

    print("🟡 Pregunta del usuario:", pregunta_usuario)
    print("🟢 Pregunta más cercana:", resultados["documents"][0][0])
    print(f"📊 Distancia Chroma: {similitud:.4f}")

    if similitud < umbral:
        return resultado["respuesta"]
    else:
        return "Lo siento, no tengo una respuesta clara para eso. Intenta reformular tu pregunta."

# API del chatbot
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    pregunta = data.get("pregunta", "")
    respuesta = encontrar_respuesta(pregunta)
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(port=5001)

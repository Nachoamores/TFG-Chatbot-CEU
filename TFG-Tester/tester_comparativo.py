import requests
import json
import difflib
import time
from collections import defaultdict

# Cargar dataset enriquecido
with open("dataset_enriquecido.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

# URLs de tus dos APIs
URL_EMBEDDINGS = "http://127.0.0.1:5001/api/chatbot"
URL_SPACY = "http://127.0.0.1:5000/api/chatbot"

# Función de similitud
def respuestas_similares(resp1, resp2, umbral=0.7):
    if resp1 is None or resp2 is None:
        return False
    similitud = difflib.SequenceMatcher(None, str(resp1).lower(), str(resp2).lower()).ratio()
    return similitud >= umbral

# Inicialización de resultados
resultados = {
    "embeddings": defaultdict(lambda: {"aciertos": 0, "fallos": 0}),
    "spacy": defaultdict(lambda: {"aciertos": 0, "fallos": 0})
}

# Matriz de confusión y tiempos
metricas = {
    "embeddings": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "tiempos": []},
    "spacy": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "tiempos": []}
}

# Evaluación
for caso in dataset:
    pregunta = caso["pregunta"]
    esperada = caso.get("respuesta", None)
    categoria = caso.get("categoria", "desconocida")

    # EMBEDDINGS
    t0 = time.time()
    try:
        response_embed = requests.post(URL_EMBEDDINGS, json={"pregunta": pregunta})
        respuesta_embed = response_embed.json().get("respuesta", None)
    except:
        respuesta_embed = None
    t1 = time.time()
    metricas["embeddings"]["tiempos"].append(t1 - t0)

    # SPACY
    t0 = time.time()
    try:
        response_spacy = requests.post(URL_SPACY, json={"pregunta": pregunta})
        respuesta_spacy = response_spacy.json().get("respuesta", None)
    except:
        respuesta_spacy = None
    t1 = time.time()
    metricas["spacy"]["tiempos"].append(t1 - t0)

    # Evaluación embeddings
    if esperada is None:
        if respuesta_embed is None or respuesta_embed.strip() == "" or "no tengo una respuesta" in str(respuesta_embed).lower():
            resultados["embeddings"][categoria]["aciertos"] += 1
            metricas["embeddings"]["TN"] += 1
        else:
            resultados["embeddings"][categoria]["fallos"] += 1
            metricas["embeddings"]["FP"] += 1
    else:
        if respuestas_similares(respuesta_embed, esperada):
            resultados["embeddings"][categoria]["aciertos"] += 1
            metricas["embeddings"]["TP"] += 1
        else:
            resultados["embeddings"][categoria]["fallos"] += 1
            metricas["embeddings"]["FN"] += 1

    # Evaluación spacy
    if esperada is None:
        if respuesta_spacy is None or respuesta_spacy.strip() == "" or "no tengo una respuesta" in str(respuesta_spacy).lower():
            resultados["spacy"][categoria]["aciertos"] += 1
            metricas["spacy"]["TN"] += 1
        else:
            resultados["spacy"][categoria]["fallos"] += 1
            metricas["spacy"]["FP"] += 1
    else:
        if respuestas_similares(respuesta_spacy, esperada):
            resultados["spacy"][categoria]["aciertos"] += 1
            metricas["spacy"]["TP"] += 1
        else:
            resultados["spacy"][categoria]["fallos"] += 1
            metricas["spacy"]["FN"] += 1

# RESULTADOS POR CATEGORÍA
for modelo in resultados:
    print(f"\nMODELO: {modelo.upper()}")
    for categoria, data in resultados[modelo].items():
        total = data["aciertos"] + data["fallos"]
        porcentaje = (data["aciertos"] / total) * 100 if total > 0 else 0
        print(f"- {categoria.title()}: {data['aciertos']} aciertos / {total} preguntas -> {porcentaje:.2f}%")

# MATRIZ DE CONFUSIÓN Y TIEMPOS
for modelo in metricas:
    print(f"\nMATRIZ DE CONFUSIÓN - {modelo.upper()}")
    print(f"TP: {metricas[modelo]['TP']} | FP: {metricas[modelo]['FP']} | TN: {metricas[modelo]['TN']} | FN: {metricas[modelo]['FN']}")
    tiempos = metricas[modelo]["tiempos"]
    promedio = sum(tiempos) / len(tiempos)
    print(f"Tiempo medio de respuesta: {promedio*1000:.2f} ms")

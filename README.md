# TFG - Chatbot CEU

Este repositorio contiene el código fuente del Trabajo de Fin de Grado (TFG) titulado:

### “Desarrollo de un chatbot para asistencia y resolución de dudas de estudiantes universitarios”

El objetivo del proyecto es crear un sistema conversacional que permita a los alumnos del CEU resolver de forma rápida y autónoma sus dudas más frecuentes, a través de un chatbot accesible desde una interfaz web. Se han implementado dos versiones diferentes del sistema, cada una basada en un enfoque distinto de procesamiento del lenguaje natural (PLN), con el fin de compararlas en términos de eficacia, precisión, escalabilidad y tiempo de respuesta.

---

## 📁 Estructura del repositorio

TFG/
├── TFG-Embeddings/            # Chatbot usando embeddings y búsqueda semántica con ChromaDB
│   ├── chatbot/
│   │   ├── api.py
│   │   └── faq_data.json
│   └── web/                   # Interfaz web HTML/CSS
├── TFG-Spacy/                 # Chatbot basado en spaCy y similitud de texto
│   ├── chatbot/
│   │   ├── api.py
│   │   └── faq_data.json
│   └── web/
├── TFG-Tester/                # Script comparador entre ambos métodos
│   ├── dataset_enriquecido.json
│   └── tester_comparativo.py
├── data/                      # Datos adicionales (por ejemplo, documentos útiles)
├── Word/                      # Documento del TFG
└── README.md


---

## ⚙️ Tecnologías utilizadas

- **Lenguaje**: Python 3.12
- **Librerías NLP**: spaCy, SentenceTransformers
- **Motor de búsqueda vectorial**: ChromaDB
- **Backend**: Flask + API REST
- **Frontend**: HTML5 + CSS3
- **Testing**: Script propio en Python con métricas y logging

---

## 🧠 Descripción de los enfoques

### 🔹 Versión 1: spaCy
Un modelo clásico de PLN utilizando `spaCy`, enfocado en el reconocimiento de entidades, tokenización y comparación textual mediante similitud. Esta versión se basa en reglas y técnicas básicas de procesamiento lingüístico.

### 🔸 Versión 2: Embeddings
Utiliza el modelo `all-MiniLM-L6-v2` de SentenceTransformers para transformar las preguntas en vectores. Se combina con una base de datos vectorial ChromaDB para realizar búsquedas semánticas, permitiendo encontrar coincidencias aunque el texto no sea exacto.

---

## 🧪 Comparativa y evaluación

Se ha implementado un script de evaluación (`tester_comparativo.py`) que compara ambas versiones usando un dataset de prueba enriquecido.

**Métricas calculadas:**
- Aciertos
- Fallos
- Tiempo medio de respuesta
- Matriz de confusión (TP, FP, TN, FN)

Estas métricas permiten evaluar cuál de las dos versiones ofrece mejores resultados en términos de comprensión semántica y rendimiento.

---

## 🖥️ Cómo ejecutar el proyecto

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Nachoaamores/TFG-Chatbot-CEU.git

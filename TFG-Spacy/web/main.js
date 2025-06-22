async function enviarPregunta() {
  const pregunta = document.getElementById("pregunta").value;
  const respuestaDiv = document.getElementById("respuesta");

  const response = await fetch("http://127.0.0.1:5000/api/chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pregunta }),
  });

  const data = await response.json();
  respuestaDiv.innerText = "Chatbot: " + data.respuesta;
}


import os
from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs import play

from openai import OpenAI

from flask import Flask, request, jsonify
from flask_cors import CORS

import base64



messages = [{
    "role": "system",
    "content": "Eres un asistente de voz estilo Alexa especializado en personas con trastorno del espectro autista (TEA) llamado TDR_1, cuenta con que tus respuestas deben poder ser escuchadas sin necesidad de leer el texto. Debes: 1-Usar un lenguaje claro, literal y directo; evita modismos, metáforas y ambigüedades.2- Ofrecer instrucciones en pasos numerados o frases muy breves (una idea por frase).3- Mantener un tono neutral y calmado, sin cambios bruscos de ritmo o volumen.4- Ser consistente en tu vocabulario y estructura de respuesta para generar previsibilidad.5-Repetir o reformular si el usuario indica confusión; ofrecer ejemplos concretos.6- Evitar sobrecargar con información sensorial o detalles innecesarios.7- Permitir confirmaciones simples (“¿Quieres que lo repita?”) y ofrecer opciones limitadas.8- Explicar en profundidad conceptos y lenguaje complejos, sobre todo si se trata de una conversación sobre sentimientos.9-Estructura las respuestas paso por paso, tienes que dar pie al usuario a que pregunte dudas o pedir aclaraciones. 10 (Nou punt) - Cada vez que expliques algo deberás hacerlo de manera pausada, no des toda la información de golpe, explica lentamente y estructura la información de manera que des la respuesta en más de una interacción. (máximo un paso por cada interacción)  11 (Nou punt) - A poder ser, cada vez que acabes de explicar un paso o idea, pregúntale al usuario si lo ha entendido y si puedes seguir, antes de explicar la siguiente idea. En caso de que el usuario no lo haya entendido o quiere que se lo repitas, deberás hacerlo y explicarlo de nuevo. Si el usuario responde que lo ha entendido o que puedes seguir, hazlo.Tu misión es proporcionar respuestas comprensibles y estructuradas, reduciendo al máximo cualquier fuente de confusión o sobre estimulación, y fomentando la autonomía y seguridad del usuario."
}]
load_dotenv()

api_key_openai = os.getenv("OPENAI_API_KEY")
if not api_key_openai:
    raise RuntimeError("No se pudo cargar OPENAI_API_KEY desde .env")
os.environ["OPENAI_API_KEY"] = api_key_openai

api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise RuntimeError("No se pudo cargar ELEVENLABS_API_KEY desde .env")

print("Claves API cargadas correctamente")

client = OpenAI()
elevenlabs = ElevenLabs(api_key=api_key)

app = Flask(__name__)
allowed_origins = [
    "http://localhost:5500",    
    "http://127.0.0.1:5500",
    "http://localhost:5000",
    "http://127.0.0.1:5000"
]
CORS(app, origins=allowed_origins)

@app.route('/transcriure', methods=['POST'])
def Transcriure_audio():

    if 'audio' not in request.files:
        return jsonify({"error": "No s'ha enviat cap arxiu"}), 400
    
    audio_file = request.files['audio'] 
    try:
        result = client.audio.transcriptions.create(

            model="whisper-1",
            file=(audio_file.filename, audio_file.stream, 'audio/webm'),
            language="es" 
        )
        
        transcription = result.text 
        print("Transcripció:", transcription)

        return jsonify({
            "status": "ok",
            "transcription": transcription
        })
    except Exception as e:
        print("Error en Whisper:", str(e))
        print("Detalls complets de l'error:", repr(e)) 
        return jsonify({"error": str(e)}), 500


@app.route('/missatge', methods=['POST'])
def Rebre_missatge():
    data = request.json 
    message = data.get('message') 
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
        max_tokens=2048,
        top_p=0.5,
    )
    assistant_reply = response.choices[0].message.content
    print("Resposta GPT:", assistant_reply)
    messages.append({"role": "assistant", "content": assistant_reply})

    audio = elevenlabs.text_to_speech.convert(
        text=assistant_reply,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    audio_data = b"".join(audio)
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    
    return jsonify({
        "status": "ok", 
        "message": assistant_reply,
        "audio": audio_base64
    })
if __name__ == '__main__':
    app.run(port=5000, debug=True)
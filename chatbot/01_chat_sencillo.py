from openai import OpenAI
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

msg = "Hola, ¿cómo estás?"

"""
Esta función es un decorador que intenta obtener una respuesta del modelo GPT-4o-mini hasta 3 veces, con un tiempo de espera aleatorio entre 4 y 15 segundos.
"""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, min=4, max=15),
)
def get_response(msg):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": msg,
            }
        ],
        temperature=0.5,
        max_tokens=50,
    )
    return response.choices[0].message.content


print(get_response(msg))

import aiohttp
import openai
import os

client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_assistant_response(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⛔ Ошибка запроса к OpenAI: {e}")
        return "Произошла ошибка при обработке запроса"
    
    
async def generate_speech(text: str, output_path: str = "temp/response.mp3"):
    try:
        response = await client.audio.speech.create(
            model="tts-1",
            voice="echo",  # alloy echo fable onyx nova shimmer
            input=text
        )
        
        audio_data = response.content

        with open(output_path, "wb") as f:
            f.write(audio_data)

        return output_path
    
    except Exception as e:
        print(f"⛔ Ошибка при генерации речи: {e}")
        return None

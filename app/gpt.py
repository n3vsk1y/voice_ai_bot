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

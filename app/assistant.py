import openai
from app.config import settings

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
model = "gpt-4-turbo"

user_threads = {} # простейшее хранилище для юзеров

async def get_assistant_response(user_id: int, prompt: str) -> str:
    if user_id not in user_threads:
        thread = await client.beta.threads.create()
        user_threads[user_id] = thread.id

    thread_id = user_threads[user_id]

    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = await client.beta.threads.runs.create_and_poll(
        assistant_id=settings.OPENAI_ASSISTANT_ID,
        thread_id=thread_id,
    )

    if run.status == 'completed': 
        messages = await client.beta.threads.messages.list(thread_id=thread_id)

        if messages:
            response_message = messages.data[0].content[0].text.value
            return response_message
        
    return run.status
    
    
async def generate_speech(text: str, filename: str) -> str:
    output_path = f"temp/{filename}_response.mp3"

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

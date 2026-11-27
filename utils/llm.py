import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not GROQ_API_KEY:
    raise Exception('❌ GROQ_API_KEY not found in .env file!')

client = Groq(api_key=GROQ_API_KEY)

def call_llm(prompt, timeout=60):
    """
    Call Groq API

    Args:
        prompt (str): The prompt to send
        timeout (int): Timeout in seconds (not used with Groq)

    Returns:
        str: LLM response
    """
    try:
        print('📡 Sending to Groq API...')

        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.choices[0].message.content.strip()

    except Exception as error:
        print(f'❌ Groq Error: {str(error)}')
        raise Exception(f'LLM Error: {str(error)}')

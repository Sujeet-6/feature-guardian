from google import genai
from guardian.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)
print(client.models.generate_content(model=GEMINI_MODEL, contents="Reply with one word: ready").text)
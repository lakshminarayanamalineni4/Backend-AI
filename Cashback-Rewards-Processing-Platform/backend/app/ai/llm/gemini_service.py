import google.generativeai as genai
from app.core.config import settings

# Authenticate the SDK once at import time so every call below reuses the
# same configured credentials instead of re-authenticating per request.
genai.configure(
    api_key=settings.GEMINI_API_KEY
)

# A single shared model instance is enough; it is stateless across calls,
# so we create it once rather than on every generate_response() invocation.
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_response(prompt: str):
    # Send the prompt to Gemini and return only the plain-text answer,
    # hiding the SDK's richer response object from callers.
    response = model.generate_content(prompt)

    return response.text

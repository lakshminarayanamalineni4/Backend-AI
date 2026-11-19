from app.ai.llm.gemini_service import generate_response

# Simple manual smoke test: run this file directly to confirm the Gemini
# integration is wired up correctly (valid API key, reachable model, etc.)
# before relying on it elsewhere in the app.
if __name__ == "__main__":
    response = generate_response("Explain Retrieval-Augmented Generation in 3 sentences.")

    print("Gemini Response:")
    print(response)

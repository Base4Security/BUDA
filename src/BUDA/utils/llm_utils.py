import openai
import requests
import re
from flask import jsonify
from ..utils.config_utils import load_llm_config

def get_llm_response(messages, model="gpt-3.5-turbo", provider="openai"):
    """
    Sends a request to the selected AI model (OpenAI or LM Studio).
    
    :param messages: List of messages to send as context.
    :param model: Model name (default: "gpt-3.5-turbo").
    :param provider: Choose between "openai" (default) or "lmstudio".
    :return: Processed AI response.
    """
    try:
        config = load_llm_config()
        provider = config["provider"]
        model = config["model_name"]
        api_key = config["api_key"] if provider == "openai" else None
        lmstudio_url = config["lmstudio_url"] if provider == "lmstudio" else "http://localhost:1234/v1/chat/completions"

        if provider == "openai":
            openai.api_key = api_key
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            result = response.choices[0].message.content.strip()

        elif provider == "lmstudio":
            LM_STUDIO_URL = lmstudio_url

            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            }

            response = requests.post(LM_STUDIO_URL, json=payload)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        else:
            return jsonify({"error": "Invalid LLM provider selected"}), 400

        # Clean and extract JSON if needed
        cleaned_result = re.sub(r"```json\s*|\s*```", "", result, flags=re.IGNORECASE)
        return cleaned_result

    except Exception as e:
        print(f"LLM request error: {e}")
        return jsonify({"error": str(e)}), 500

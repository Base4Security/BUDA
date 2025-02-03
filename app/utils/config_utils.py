import os
import json
from flask import jsonify

CONFIG_FILE = "config_llm.json"

def load_llm_config():
    """Loads LLM settings from a JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return jsonify({"error": "No LLM settings found"}), 404
    
def save_llm_config(new_config):
    """Saves llm settings to a JSON file."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(new_config, file, indent=4)
        return {"message": "Settings updated successfully"}
    except Exception as e:
        return {"error": str(e)}
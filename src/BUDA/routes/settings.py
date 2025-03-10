from flask import Blueprint, request, render_template, jsonify
from ..utils.config_utils import load_llm_config, save_llm_config
from ..utils.init_db_util import recreate_database

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/', methods=['GET', 'POST'])
def manage_settings():
    """Handles AI settings (choose provider, model, API key)."""
    if request.method == 'POST':
        data = request.form
        new_config = {
            "provider": data.get('provider', 'openai'),
            "model_name": data.get('model_name', 'gpt-3.5-turbo'),
            "api_key": data.get('api_key', '') if data.get('provider') == 'openai' else "",
            "lmstudio_url": data.get('lmstudio_url', 'http://localhost:1234/v1/chat/completions')
        }
        save_llm_config(new_config)
        return jsonify({"message": "Settings updated successfully"}), 200

    config = load_llm_config()
    return render_template('settings.html', settings=config)

@settings_bp.route('/reset_db', methods=['POST'])
def reset_db():
    
    """API endpoint to reset the database."""
    result = recreate_database()

    return jsonify(result)
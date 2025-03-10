from flask import Blueprint, render_template, jsonify
from ..models.narrative import Narrative

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def home():
    # Fetch narratives from the database
    try:
        narratives = Narrative.query.all()
    except:
        return jsonify({"error": "Something is wrong or Database table missing. Recreate it on /settings`."}), 500
    
    #return render_template('home.html')
    return render_template('home.html', narratives=narratives)
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.narrative import Narrative
from app import db
import requests
import json
from datetime import datetime

narratives_bp = Blueprint('narratives_bp', __name__)

@narratives_bp.route('/', methods=['GET', 'POST'])
def manage_narratives():
    if request.method == 'POST':
        # Handle narrative creation
        title = request.form.get('title')
        objective = request.form.get('objective')
        attacker_profile = request.form.get('attacker_profile')
        deception_activities = request.form.get('deception_activities')
        end_date_str = request.form.get('end_date')
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Save the narrative (example)
        new_narrative = Narrative(
            title=title,
            objective=objective,
            attacker_profile=attacker_profile,
            deception_activities=deception_activities,
            end_date=end_date
        )
        db.session.add(new_narrative)
        db.session.commit()
        return redirect(url_for('narratives_bp.manage_narratives'))

    # Fetch attacker profiles from the database
    try:
        narratives = Narrative.query.all()
    except:
        return jsonify({"error": "Something is wrong or Database table missing. Recreate it on /settings`."}), 500
    return render_template('narratives.html', narratives=narratives)

@narratives_bp.route('/delete/<int:narrative_id>', methods=['POST'])
def delete_narrative(narrative_id):
    narrative = Narrative.query.get_or_404(narrative_id)
    db.session.delete(narrative)
    db.session.commit()
    return redirect(url_for('narratives_bp.manage_narratives'))

@narratives_bp.route('/edit/<int:narrative_id>', methods=['GET', 'POST'])
def edit_narrative(narrative_id):
    # Obtener la narrativa existente
    narrative = Narrative.query.get_or_404(narrative_id)

    if request.method == 'POST':
        # Actualizar los datos de la narrativa
        narrative.title = request.form.get('title')
        narrative.objective = request.form.get('objective')
        narrative.attacker_profile = request.form.get('attacker_profile')
        narrative.deception_activities = request.form.get('deception_activities')
        end_date_str = request.form.get('end_date')
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        narrative.end_date = end_date


        db.session.commit()
        return redirect(url_for('narratives_bp.manage_narratives'))

    # Renderizar el formulario de edición con los datos de la narrativa
    return render_template('narrative_edit.html', narrative=narrative)

@narratives_bp.route('/generate', methods=['POST'])
def generate_narrative():
    response = requests.post("http://localhost:5000/ai/generate", json={"section": "narrative"})
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate narrative"}), 500
    try:
        narrative_data = json.loads(response.json()["response"])
        new_narrative = Narrative(
            title=narrative_data['Title'],
            objective=narrative_data['Objective'],
            attacker_profile=narrative_data['Attacker Profile'],
            end_date=int(narrative_data['End Date']),
        )
        db.session.add(new_narrative)
        db.session.commit()
        return jsonify({"message": "Narrative generated and saved successfully", "narrative": narrative_data}), 200
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid response format from AI"}), 400
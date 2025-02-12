from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, send_file
from app.models.narrative import Narrative
from app import db
import requests
import json
from datetime import datetime
from app.utils.narrative_worker import start_narrative, stop_narrative
import time
import os

narratives_bp = Blueprint('narratives_bp', __name__)

@narratives_bp.route('/', methods=['GET', 'POST'])
def manage_narratives():
    if request.method == 'POST':
        # Handle narrative creation
        title = request.form.get('title')
        objective = request.form.get('objective')
        attacker_profile = request.form.get('attacker_profile')
        deception_activities = request.form.get('deception_activities')
        percentage_of_similarity = request.form.get('percentage_of_similarity')
        end_date_str = request.form.get('end_date')
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        is_running = False
        winrm_server = request.form.get('winrm_server')
        winrm_username = request.form.get('winrm_username')
        winrm_password = request.form.get('winrm_password')

        # Save the narrative (example)
        new_narrative = Narrative(
            title=title,
            objective=objective,
            attacker_profile=attacker_profile,
            deception_activities=deception_activities,
            percentage_of_similarity=percentage_of_similarity,
            winrm_server=winrm_server,
            winrm_username=winrm_username,
            winrm_password=winrm_password,
            end_date=end_date,
            is_running=is_running
        )
        db.session.add(new_narrative)
        db.session.commit()
        return redirect(url_for('narratives_bp.manage_narratives'))

    # Fetch narratives from the database
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
        narrative.percentage_of_similarity = request.form.get('percentage_of_similarity')
        end_date_str = request.form.get('end_date')
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        narrative.end_date = end_date
        narrative.winrm_server = request.form.get('winrm_server')
        narrative.winrm_username = request.form.get('winrm_username')
        narrative.winrm_password = request.form.get('winrm_password')

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

@narratives_bp.route('/start/<int:narrative_id>', methods=['POST'])
def start_narrative_route(narrative_id):
    # Starts a narrative.
    result = start_narrative(narrative_id)
    return jsonify(result)

@narratives_bp.route('/stop/<int:narrative_id>', methods=['POST'])
def stop_narrative_route(narrative_id):
    # Stops a narrative.
    result = stop_narrative(narrative_id)
    return jsonify(result)

# Streaming Logs

LOG_DIR = os.path.abspath("logs")

def get_latest_log_files():
    """
    Returns a list of the latest log file(s) based on the current date and hour.
    If no logs are found for the current hour, fetches from the previous hour.
    """
    files = [os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if f.endswith(".log")]
    files.sort(reverse=True)
    return files[:2]

def event_stream():
    #Yields real-time execution logs from the latest available log files
    last_lines = []

    while True:
        log_files = get_latest_log_files()
        log_files.sort(reverse=False)
        all_logs = []
        # Read from multiple log files (current & previous hour if needed)
        for log_file in log_files:
            with open(log_file, "r") as file:
                all_logs.extend(file.readlines())

        last_lines = all_logs[-20:]
        last_lines.reverse()

        if last_lines:
            for line in last_lines:
                yield f"data: {line.strip()}\n\n"
        
        time.sleep(5)

@narratives_bp.route('/stream')
def stream_logs():
    """Streams real-time execution logs from time-based log files."""
    return Response(event_stream(), mimetype="text/event-stream")

def get_latest_log_filename():
    """
    Returns the latest log file based on the current hour.
    """
    now = datetime.now()
    log_filename = os.path.join(LOG_DIR, now.strftime("%Y-%m-%d_%H") + ".log")
    print
    print(log_filename)
    if os.path.exists(log_filename):
        return log_filename
    else:
        return None  # No log file found for the current hour
    
@narratives_bp.route('/download-log', methods=['GET'])
def download_log():
    """Allows users to download the log file for the last hour."""
    log_file = get_latest_log_filename()
    print(log_file)
    if log_file:
        return send_file(log_file, as_attachment=True)
    else:
        return jsonify({"error": "No log file available for this hour."}), 404
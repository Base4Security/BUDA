from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.user import UserProfile
from app.models.narrative import Narrative
from app import db
import json
import requests


user_profiles_bp = Blueprint('user_profiles_bp', __name__)

@user_profiles_bp.route('/', methods=['GET', 'POST'])
def manage_user_profiles():
    if request.method == 'POST':
        # Recibir datos del formulario
        name = request.form.get('name')
        role = request.form.get('role')
        behavior_pattern = request.form.get('behavior_pattern')
        narrative_id = int(request.form.get('narrative_id'))

        # Crear y guardar el perfil ficticio
        new_user_profile = UserProfile(
            name=name,
            role=role,
            behavior_pattern=behavior_pattern,
            narrative_id=narrative_id
        )
        db.session.add(new_user_profile)
        db.session.commit()

        return redirect(url_for('user_profiles_bp.manage_user_profiles'))

    # Obtener todos los perfiles y narrativas para mostrarlos
    user_profiles = UserProfile.query.all()
    narratives = Narrative.query.all()
    return render_template('user_profiles.html', user_profiles=user_profiles, narratives=narratives)

@user_profiles_bp.route('/edit/<int:user_profile_id>', methods=['GET', 'POST'])
def edit_user_profile(user_profile_id):
    user_profile = UserProfile.query.get_or_404(user_profile_id)

    if request.method == 'POST':
        # Actualizar datos del perfil
        user_profile.name = request.form.get('name')
        user_profile.role = request.form.get('role')
        user_profile.behavior_pattern = request.form.get('behavior_pattern')
        user_profile.narrative_id = int(request.form.get('narrative_id'))

        db.session.commit()
        return redirect(url_for('user_profiles_bp.manage_user_profiles'))

    # Renderizar el formulario de edición con los datos del perfil
    narratives = Narrative.query.all()
    return render_template('edit_user_profile.html', user_profile=user_profile, narratives=narratives)

@user_profiles_bp.route('/delete/<int:user_profile_id>', methods=['POST'])
def delete_user_profile(user_profile_id):
    user_profile = UserProfile.query.get_or_404(user_profile_id)
    db.session.delete(user_profile)
    db.session.commit()
    return redirect(url_for('user_profiles_bp.manage_user_profiles'))

@user_profiles_bp.route('/generate', methods=['POST'])
def generate_user_profile():
    data = request.json
    narrative_id = data.get('narrative_id')
    response = requests.post("http://localhost:5000/ai/generate", json={"section": "user_profile"})
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate user profile"}), 500
    try:
        profile_data = json.loads(response.json()["response"])
        new_profile = UserProfile(
            name=profile_data['Name'],
            role=profile_data['Role'],
            behavior_pattern=profile_data['Behavior Pattern'],
            narrative_id=narrative_id
        )
        db.session.add(new_profile)
        db.session.commit()
        return jsonify({"message": "User Profile generated and saved successfully", "profile": profile_data}), 200
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid response format from AI"}), 400
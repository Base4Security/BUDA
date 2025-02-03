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
    try:
        user_profiles = UserProfile.query.all()
        narratives = Narrative.query.all()
    except:
        return jsonify({"error": "Something is wrong or Database table missing. Recreate it on /settings`."}), 500
        
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
    
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..models.user import UserProfile
from ..models.narrative import Narrative
from ..app import db

user_profiles_bp = Blueprint('user_profiles_bp', __name__)

@user_profiles_bp.route('/', methods=['GET', 'POST'])
def manage_user_profiles():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        role = request.form.get('role')
        behavior_pattern = request.form.get('behavior_pattern')
        winrm_server = request.form.get('winrm_server')
        winrm_username = request.form.get('winrm_username')
        winrm_password = request.form.get('winrm_password')

        narratives_id = request.form.getlist('narratives_id')
        narratives = Narrative.query.filter(Narrative.id.in_(narratives_id)).all()

        # Create and save the user profile
        new_user_profile = UserProfile(
            name=name,
            role=role,
            behavior_pattern=behavior_pattern,
            winrm_server=winrm_server,
            winrm_username=winrm_username,
            winrm_password=winrm_password,
        )
        new_user_profile.narrative = narratives

        db.session.add(new_user_profile)
        db.session.commit()

        return redirect(url_for('user_profiles_bp.manage_user_profiles'))

    try:
        user_profiles = UserProfile.query.all()
        all_narratives = Narrative.query.all()
    except:
        return jsonify({"error": "Something is wrong or Database table missing. Recreate it on /settings`."}), 500
    
    return render_template('user_profiles.html', user_profiles=user_profiles, all_narratives=all_narratives)

@user_profiles_bp.route('/edit/<int:user_profile_id>', methods=['GET', 'POST'])
def edit_user_profile(user_profile_id):
    user_profile = UserProfile.query.get_or_404(user_profile_id)

    if request.method == 'POST':
        # Get data from the form
        user_profile.name = request.form.get('name')
        user_profile.role = request.form.get('role')
        user_profile.behavior_pattern = request.form.get('behavior_pattern')
        user_profile.winrm_server = request.form.get('winrm_server')
        user_profile.winrm_username = request.form.get('winrm_username')
        user_profile.winrm_password = request.form.get('winrm_password')
        # Handle multiple Narratives
        narratives_id = request.form.getlist('narratives_id')
        narratives = Narrative.query.filter(Narrative.id.in_(narratives_id)).all()
        user_profile.narrative = narratives

        db.session.commit()
        return redirect(url_for('user_profiles_bp.manage_user_profiles'))

    all_narratives = Narrative.query.all()

    return render_template('edit_user_profile.html', user_profile=user_profile, all_narratives=all_narratives)

@user_profiles_bp.route('/delete/<int:user_profile_id>', methods=['POST'])
def delete_user_profile(user_profile_id):
    user_profile = UserProfile.query.get_or_404(user_profile_id)
    db.session.delete(user_profile)
    db.session.commit()
    return redirect(url_for('user_profiles_bp.manage_user_profiles'))

@user_profiles_bp.route('/list', methods=['GET'])
def list_user_profiles():
    """Returns a list of all user profiles."""
    profiles = UserProfile.query.all()
    return jsonify({"user_profiles": [profile.to_dict() for profile in profiles]})
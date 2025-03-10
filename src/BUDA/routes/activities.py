from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..models.activity import Activity
from ..models.user import UserProfile
from ..app import db
import requests
import json

activities_bp = Blueprint('activities_bp', __name__)

@activities_bp.route('/', methods=['GET', 'POST'])
def manage_activities():
    if request.method == 'POST':
        # Get data from the form
        activity_type = request.form.get('activity_type')
        details = request.form.get('details')

        # Handle User Profiles (Multiple)
        user_profile_ids = request.form.getlist('user_profiles')
        user_profiles = UserProfile.query.filter(UserProfile.id.in_(user_profile_ids)).all()

        # Crear y guardar la actividad
        new_activity = Activity(
            activity_type=activity_type,
            details=details,
        )

        new_activity.user_profiles = user_profiles

        db.session.add(new_activity)
        db.session.commit()

        return redirect(url_for('activities_bp.manage_activities'))

    # Fetch all activities and user profiles
    try:
        all_activities = Activity.query.all()
        all_user_profiles = UserProfile.query.all()
    except:
        return jsonify({"error": "Something is wrong or Database table missing. Recreate it on /settings`."}), 500
       
    return render_template('activities.html', all_activities=all_activities, all_user_profiles=all_user_profiles)

@activities_bp.route('/edit/<int:activity_id>', methods=['GET', 'POST'])
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    all_user_profiles = UserProfile.query.all()

    if request.method == 'POST':
        # Update the activity
        activity.activity_type = request.form.get('activity_type')
        activity.details = request.form.get('details')
        # Handle User Profiles (Multiple)
        user_profile_ids = request.form.getlist('user_profiles')
        user_profiles = UserProfile.query.filter(UserProfile.id.in_(user_profile_ids)).all()
        activity.user_profiles = user_profiles

        db.session.commit()
        return redirect(url_for('activities_bp.manage_activities'))

    # Render the edit form
    return render_template('edit_activities.html', activity=activity, all_user_profiles=all_user_profiles)

@activities_bp.route('/delete/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for('activities_bp.manage_activities'))

@activities_bp.route('/generate', methods=['POST'])
def generate_activity():
    data = request.json
    user_profile_id = data.get('user_profile_id')
    response = requests.post("http://localhost:5000/ai/generate", json={"section": "activity"})
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate activity"}), 500
    try:
        profile_data = json.loads(response.json()["response"])
        
        # Recursive function to find keys regardless of case
        def search_keys(obj):
            activity_type = None
            details = None
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_lower = key.lower()
                    if key_lower == "activity_type":
                        activity_type = value
                    elif key_lower == "details":
                        details = value
                    elif isinstance(value, (dict, list)):
                        # Recursively search nested objects or lists
                        sub_result = search_keys(value)
                        activity_type = activity_type or sub_result.get("activity_type")
                        details = details or sub_result.get("details")
            elif isinstance(obj, list):
                for item in obj:
                    sub_result = search_keys(item)
                    activity_type = activity_type or sub_result.get("activity_type")
                    details = details or sub_result.get("details")
            
            return {"activity_type": activity_type, "details": details}

        # Search for the keys in the parsed data
        result = search_keys(profile_data)

        activity_type = result["activity_type"]
        details = result["details"]

        new_profile = Activity(
            activity_type=activity_type,
            details=details,
            user_profile_id=user_profile_id
        )
        db.session.add(new_profile)
        db.session.commit()
        return jsonify({"message": "User Profile generated and saved successfully", "profile": profile_data}), 200
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid response format from AI"}), 400
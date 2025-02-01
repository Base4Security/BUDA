from flask import Blueprint, jsonify, render_template
from app.models.narrative import Narrative
from app.models.user import UserProfile
from app.models.activity import Activity
from sqlalchemy import func
from app import db

statistics_bp = Blueprint('statistics_bp', __name__)

@statistics_bp.route('/activities_per_narrative', methods=['GET'])
def activities_per_narrative():
    # Explicit join conditions
    data = db.session.query(
        Narrative.title.label("narrative_title"),  # Alias for clarity
        func.count(Activity.id).label("activity_count")
    ).join(UserProfile, UserProfile.narrative_id == Narrative.id
           ).join(Activity, Activity.user_profile_id == UserProfile.id
                  ).group_by(Narrative.title).all()

    # Format the result for JSON
    result = [{"narrative": row.narrative_title, "activities": row.activity_count} for row in data]
    return jsonify(result)

@statistics_bp.route('/activities_per_profile', methods=['GET'])
def activities_per_profile():
    # Consulta para contar actividades por perfil ficticio
    data = db.session.query(
        UserProfile.name,
        func.count(Activity.id)
    ).join(Activity).group_by(UserProfile.name).all()

    # Formatear para JSON
    result = [{"profile": row[0], "activities": row[1]} for row in data]
    return jsonify(result)

@statistics_bp.route('/dashboard', methods=['GET'])
def statistics_dashboard():
    return render_template('statistics.html')

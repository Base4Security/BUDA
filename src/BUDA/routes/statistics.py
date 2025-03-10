from flask import Blueprint, jsonify, render_template
from sqlalchemy import func
from ..app import db

from ..models.narrative import Narrative
from ..models.user import UserProfile
from ..models.activity import Activity
from ..models.narratives_user_profiles import narratives_user_profiles
from ..models.user_profiles_activity_types import user_profiles_activity_types


statistics_bp = Blueprint('statistics_bp', __name__)

@statistics_bp.route('/activities_per_narrative', methods=['GET'])
def activities_per_narrative():
    """
    Get the number of activities per narrative, counting activities from all user profiles assigned to each narrative.
    """
    data = db.session.query(
        Narrative.title.label("narrative_title"),
        func.coalesce(func.count(Activity.id), 0).label("activity_count")
    ).outerjoin(narratives_user_profiles, Narrative.id == narratives_user_profiles.c.narrative_id) \
     .outerjoin(UserProfile, UserProfile.id == narratives_user_profiles.c.user_profile_id) \
     .outerjoin(user_profiles_activity_types, UserProfile.id == user_profiles_activity_types.c.user_profile_id) \
     .outerjoin(Activity, Activity.id == user_profiles_activity_types.c.activity_id) \
     .group_by(Narrative.title).all()

    # Format result as JSON
    result = [{"narrative": row.narrative_title, "activities": row.activity_count} for row in data]
    return jsonify(result)

@statistics_bp.route('/activities_per_profile', methods=['GET'])
def activities_per_profile():
    """
    Count the number of activities per user profile, including profiles with 0 activities.
    """
    data = db.session.query(
        UserProfile.name.label("profile_name"),
        func.coalesce(func.count(Activity.id), 0).label("activity_count")
    ).outerjoin(user_profiles_activity_types, UserProfile.id == user_profiles_activity_types.c.user_profile_id) \
     .outerjoin(Activity, Activity.id == user_profiles_activity_types.c.activity_id) \
     .group_by(UserProfile.name).all()

    # Format result as JSON
    result = [{"profile": row.profile_name, "activities": row.activity_count} for row in data]
    return jsonify(result)

@statistics_bp.route('/narratives_per_profile', methods=['GET'])
def narratives_per_profile():
    # Query to count narratives by fictitious profile
    data = db.session.query(
        UserProfile.name.label("profile_name"),
        func.count(Narrative.id).label("narrative_count")
    ).join(narratives_user_profiles, UserProfile.id == narratives_user_profiles.c.user_profile_id) \
     .join(Narrative, Narrative.id == narratives_user_profiles.c.narrative_id) \
     .group_by(UserProfile.name) \
     .order_by(func.count(Narrative.id).desc()) \
     .all()

    # Format the result for JSON
    result = [{"profile": row.profile_name, "narratives": row.narrative_count} for row in data]
    return jsonify(result)

@statistics_bp.route('/dashboard', methods=['GET'])
def statistics_dashboard():
    
    return render_template('statistics.html')

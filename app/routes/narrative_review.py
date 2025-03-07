from flask import Blueprint, render_template, request, redirect, url_for
from app.models.narrative import Narrative
from app.models.user import UserProfile
from app.models.activity import Activity
from app import db

narrative_review_bp = Blueprint('narrative_review_bp', __name__)

@narrative_review_bp.route('/narratives/review/<int:narrative_id>', methods=['GET'])
def review_narrative(narrative_id):
    # Obtener la narrativa específica
    narrative = Narrative.query.get_or_404(narrative_id)

    # Obtener perfiles asociados a la narrativa
    user_profiles = narrative.user_profiles
    print(user_profiles)

    # Obtener actividades relacionadas con los perfiles
    activities = Activity.query.filter(Activity.user_profile_id.in_([profile.id for profile in user_profiles])).all()

    return render_template('narrative_review.html', narrative=narrative, user_profiles=user_profiles, activities=activities)

from flask import Blueprint, render_template, request, redirect, url_for
from ..models.narrative import Narrative
from ..models.user import UserProfile
from ..models.activity import Activity
from ..app import db

narrative_review_bp = Blueprint('narrative_review_bp', __name__)

@narrative_review_bp.route('/narratives/review/<int:narrative_id>', methods=['GET'])
def review_narrative(narrative_id):
    # Obtain the narrative
    narrative = Narrative.query.get_or_404(narrative_id)

    # Obtain the user
    user_profiles = narrative.user_profiles

    return render_template('narrative_review.html', narrative=narrative, user_profiles=user_profiles)

from app import db

# ✅ Many-to-Many Association Table
narratives_user_profiles = db.Table(
    'narratives_user_profiles',
    db.Column('narrative_id', db.Integer, db.ForeignKey('narratives.id'), primary_key=True),
    db.Column('user_profile_id', db.Integer, db.ForeignKey('user_profiles.id'), primary_key=True)
)
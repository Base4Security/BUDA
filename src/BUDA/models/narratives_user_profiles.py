from ..app import db

# Table for many-to-many association between Narratives and User Profiles
narratives_user_profiles = db.Table(
    'narratives_user_profiles',
    db.Column('narrative_id', db.Integer, db.ForeignKey('narratives.id'), primary_key=True),
    db.Column('user_profile_id', db.Integer, db.ForeignKey('user_profiles.id'), primary_key=True)
)
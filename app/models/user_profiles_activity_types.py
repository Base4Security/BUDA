from app import db

# ✅ Many-to-Many Association Table
user_profiles_activity_types = db.Table(
    'user_profiles_activity_types',
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
    db.Column('user_profile_id', db.Integer, db.ForeignKey('user_profiles.id'), primary_key=True)
)
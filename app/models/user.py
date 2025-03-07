from app import db
from .narratives_user_profiles import narratives_user_profiles
from .user_profiles_activity_types import user_profiles_activity_types

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    behavior_pattern = db.Column(db.Text, nullable=False)
    winrm_server = db.Column(db.String(100), nullable=False)
    winrm_username = db.Column(db.String(100), nullable=False)
    winrm_password = db.Column(db.String(100), nullable=False)

    narrative = db.relationship('Narrative', secondary=narratives_user_profiles, back_populates='user_profiles')
    activities = db.relationship('Activity', secondary=user_profiles_activity_types, back_populates='user_profiles')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'behavior_pattern': self.behavior_pattern,
            'narrative': [narrative.to_dict() for narrative in self.narrative],
            'activities': [activity.to_dict() for activity in self.activities],
            'winrm': {
                'server': self.winrm_server,
                'username': self.winrm_username,
                'password': self.winrm_password
            }
        }

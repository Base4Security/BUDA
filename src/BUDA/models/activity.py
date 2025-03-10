from ..app import db
from .user_profiles_activity_types import user_profiles_activity_types

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    activity_type = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=True)  # JSON o string con detalles adicionales

    # Relación con el perfil de usuario
    user_profiles = db.relationship('UserProfile', secondary=user_profiles_activity_types, back_populates='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'activity_type': self.activity_type,
            'details': self.details,
            'user_profiles': [profile.to_dict() for profile in self.user_profiles],
        }

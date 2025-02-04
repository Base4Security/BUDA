from app import db

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    activity_type = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=True)  # JSON o string con detalles adicionales

    # Relación con el perfil de usuario
    user_profile = db.relationship('UserProfile', back_populates='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'user_profile_id': self.user_profile_id,
            'timestamp': self.timestamp.isoformat(),
            'activity_type': self.activity_type,
            'details': self.details
        }

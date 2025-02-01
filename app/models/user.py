from app import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    behavior_pattern = db.Column(db.Text, nullable=False)  # JSON de patrones
    narrative_id = db.Column(db.Integer, db.ForeignKey('narratives.id'), nullable=False)

    narrative = db.relationship('Narrative', back_populates='user_profiles')
    activities = db.relationship('Activity', back_populates='user_profile', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'behavior_pattern': self.behavior_pattern,
            'narrative_id': self.narrative_id,
            'activities': [activity.to_dict() for activity in self.activities]
        }

from ..app import db
from .narratives_user_profiles import narratives_user_profiles

class Narrative(db.Model):
    __tablename__ = 'narratives'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    objective = db.Column(db.Text, nullable=False)
    attacker_profile = db.Column(db.Text, nullable=True)
    deception_activities = db.Column(db.Text, nullable=True)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    percentage_of_similarity = db.Column(db.Float, default=0.0)
    is_running = db.Column(db.Boolean, default=True)

    user_profiles = db.relationship('UserProfile', secondary=narratives_user_profiles, back_populates='narrative')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'objective': self.objective,
            'attacker_profile': self.attacker_profile,
            'deception_activities': self.deception_activities,
            'end_date': self.end_date.isoformat(),
            'created_at': self.created_at,
            'user_profiles': [profile.to_dict() for profile in self.user_profiles],
            'percentage_of_similarity': self.percentage_of_similarity
        }
    
    def __repr__(self):
        return f'<Narrative {self.title} Runnning: {self.is_running}>'

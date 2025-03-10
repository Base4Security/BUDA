from ..app import db

class APTGroups(db.Model):
    __tablename__ = 'aptgroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship to TTPUsed
    ttps = db.relationship('TTPUsed', backref='aptgroups', lazy=True)

class TTPUsed(db.Model):
    __tablename__ = 'ttpused'
    id = db.Column(db.Integer, primary_key=True)
    ttp = db.Column(db.String(200), nullable=False)
    
    # Foreign key linking to APTGroup
    aptgroup_id = db.Column(db.Integer, db.ForeignKey('aptgroups.id'), nullable=False)


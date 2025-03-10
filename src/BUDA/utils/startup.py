from ..models.narrative import Narrative
from ..app import db

def reset_narratives_on_startup(app):
    #Resets all narratives to `is_running = False` on app startup.
    with app.app_context():
        db.session.query(Narrative).update({Narrative.is_running: False})
        db.session.commit()
        print("All narratives have been reset to NOT running.")

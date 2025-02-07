import threading
import time
from datetime import datetime
from flask import current_app
from app import db
from app.models import Narrative

running_narratives = {}

def narrative_engine(narrative_id, app):
    """
    Simulates a background process for the narrative.
    Stops when the end date is reached or the user manually stops it.
    """
    with app.app_context():
        narrative = Narrative.query.get(narrative_id)
        if not narrative:
            return

        while narrative.is_running:
            # Check if the narrative has reached its end date
            print(f"Checking if the narrative has reached its end date...")
            if datetime.now().date() >= narrative.end_date:
                narrative.is_running = False
                db.session.commit()
                print(f"The narrative has reached its end date.")
                return
            
            # Code execution for the narrative

            print(f"Running Narrative {narrative.title}...")
            time.sleep(10)

            # End of the loop

        print(f"Narrative has been stopped manually.")

def start_narrative(narrative_id):
    """
    Starts a narrative process in a background thread.
    """
    if narrative_id in running_narratives:
        return {"error": f"Narrative is already running"}

    app = current_app._get_current_object()

    with app.app_context():
        narrative = Narrative.query.get(narrative_id)
        if not narrative:
            return {"message": f"Narrative not found"}
        
        if datetime.now().date() >= narrative.end_date:
            return {"message": f"Narrative has already reached its end date"}
        
        narrative.is_running = True
        db.session.commit()

    thread = threading.Thread(target=narrative_engine, args=(narrative_id, app))
    thread.daemon = True
    thread.start()

    running_narratives[narrative_id] = thread
    
    return {"message": f"Narrative started"}

def stop_narrative(narrative_id):
    """
    Stops a running narrative process.
    """

    app = current_app._get_current_object()

    with app.app_context():
        narrative = Narrative.query.get(narrative_id)
        if not narrative:
            return {"error": f"Narrative not found"}

        narrative.is_running = False
        db.session.commit()

    if narrative_id in running_narratives:
        del running_narratives[narrative_id]

    return {"message": f"Narrative stopped"}

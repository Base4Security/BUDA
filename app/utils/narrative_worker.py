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
            if datetime.now().date() >= narrative.end_date:
                narrative.is_running = False
                db.session.commit()
                print(f"Narrative {narrative.title} has stopped (End Date Reached).")
                return
            
            # Code execution for the narrative

            print(f"Running Narrative {narrative.title}...")
            print(f"Running: {narrative.is_running}")
            time.sleep(10)  # Simulate background task with a delay

            # End of the loop

        print(f"Narrative {narrative.title} has been stopped manually.")

def start_narrative(narrative_id):
    """
    Starts a narrative process in a background thread.
    """
    if narrative_id in running_narratives:
        return {"error": "Narrative is already running"}

    app = current_app._get_current_object()

    with app.app_context():
        narrative = Narrative.query.get(narrative_id)
        if not narrative:
            return {"error": "Narrative not found"}
        
        narrative.is_running = True
        db.session.commit()

    thread = threading.Thread(target=narrative_engine, args=(narrative_id, app))
    thread.daemon = True  # Ensures thread exits when Flask stops
    thread.start()

    running_narratives[narrative_id] = thread
    return {"message": f"Narrative {narrative_id} started"}

def stop_narrative(narrative_id):
    """
    Stops a running narrative process.
    """

    app = current_app._get_current_object()

    with app.app_context():
        narrative = Narrative.query.get(narrative_id)
        if not narrative:
            return {"error": "Narrative not found"}

        narrative.is_running = False
        db.session.commit()

    if narrative_id in running_narratives:
        del running_narratives[narrative_id]

    return {"message": f"Narrative {narrative_id} stopped"}

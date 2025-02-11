import threading
import time
from datetime import datetime
from flask import current_app
from app import db
from app.models import Narrative
from app.utils.orchestrator import execute_command


narratives_to_stop = {}

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
            # Refresh the narrative object from the database
            if narrative.id in narratives_to_stop:
                narrative.is_running = False
                db.session.commit()
                del narratives_to_stop[narrative.id]
                print(f"The narrative {narrative.id} has been stopped manually.")
                return
            
            # Check if the narrative has reached its end date
            if datetime.now().date() >= narrative.end_date:
                narrative.is_running = False
                db.session.commit()
                print(f"The narrative has reached its end date.")
                return
            
            # Code execution for the narrative
            # Add current execution date to log

            print(f"{datetime.now().date()} - Running Narrative {narrative.id} - {narrative.title} - End Date: {narrative.end_date}")

            from app.utils.behavior_engine import generate_commands
            commands = generate_commands(narrative)

            for command in commands:
                print(f"Executing command: {command}")
                output = execute_command(narrative.id, "Test", command)
                print(f"Output: {output}")

            time.sleep(10)

            # End of the loop

        print(f"Narrative has been stopped manually.")

def start_narrative(narrative_id):
    """
    Starts a narrative process in a background thread.
    """
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
        narratives_to_stop[narrative_id] = True
        print(f"Narrative {narrative_id} has been queued for stopping.")

    return {"message": f"Narrative stopped"}

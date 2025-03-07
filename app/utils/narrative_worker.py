import threading
import time
from datetime import datetime
from flask import current_app
from app import db
from app.models import Narrative
from app.utils.orchestrator import execute_command
import random


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
                return
            
            # Check if the narrative has reached its end date
            if datetime.now().date() >= narrative.end_date:
                narrative.is_running = False
                db.session.commit()
                return
            
            # Code execution for the narrative
            # Add current execution date to log

            print(f"{datetime.now().date()} - Running Narrative {narrative.id} - {narrative.title} - End Date: {narrative.end_date}")

            from app.utils.behavior_engine import generate_commands
            commands = generate_commands(narrative.id)
            
            try:
                commands = commands["commands"]
            except:
                commands = commands

            # Extract the commands
            for command_set in commands:
                user_profile = command_set["user_profile"]
                for cmd in command_set["commands"]:
                    print(f"{datetime.now().date()} - [NW]Executing command: {cmd}")
                    output = execute_command(narrative,  user_profile, cmd)
    
            # Sleep random time between 30 and 600 seconds
            sleep_time = random.randint(30, 600)
            print(f"{datetime.now().date()} - [NW]Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)

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
        
        if not narrative.user_profiles:
            return {"message": f"Narrative has no user profiles"}
        
        for narrative_user_profile in narrative.user_profiles:
            if not narrative_user_profile.activities:
                return {"message": f"User profile '{narrative_user_profile.name}' has no activity types"}

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
        return {"message": f"Narrative '{narrative.title}' queued for stopping."}

    return

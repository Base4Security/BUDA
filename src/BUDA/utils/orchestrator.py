import winrm
from datetime import datetime
from ..utils.logger import log_command
from ..models.user import UserProfile

def execute_command(narrative, user_name, command):
    """
    Executes a PowerShell command remotely via WinRM.
    """
    narrative_id = narrative.id
    winrm_server = narrative.winrm_server
    winrm_username = narrative.winrm_username
    winrm_password = narrative.winrm_password

    # Search for user_profile with user_profile.name == user_name
    user_profile = UserProfile.query.filter_by(name=user_name).first()
    if not user_profile:
        return f"User profile '{user_name}' not found"
    
    print(f"{datetime.now().date()} - [Or]User Profile: {user_profile.name}")

    try:
        print(f"{datetime.now().date()} - [Or]Executing command: {command}")
        session = winrm.Session(winrm_server, auth=(winrm_username, winrm_password))
        response = session.run_ps(command)
        print(f"{datetime.now().date()} - [Or]Response: {response.status_code}")
        log_command(narrative_id, user_profile, command, response.status_code)
        if response.status_code == 0:
            print(response.std_out.decode('utf-8').strip())
            return response.std_out.decode('utf-8').strip()
        else:
            print(f"{datetime.now().date()} - [Or]Response error: {response.status_code}")
            return f"Error: {response.std_err.decode('utf-8').strip()}"
    except Exception as e:
        print(f"{datetime.now().date()} - [Or]WinRM Error: {str(e)}")
        log_command(narrative_id, user_profile, command, str(e))
        return f"WinRM Error: {str(e)}"

    # Log the command execution
    # narrative_id = 1
    # user_profile = "user1"
    # output = "Output of the command"
    # log_command(narrative_id, user_profile, command, output)
    # 
    # return "WinRM not implemented yet"
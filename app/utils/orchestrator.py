import winrm
from app.utils.logger import log_command


# WINRM Configuration
WINRM_SERVER = "http://remote-server:5985/wsman"
WINRM_USERNAME = "admin"
WINRM_PASSWORD = "YourSecurePassword"

def execute_command(narrative_id, user_profile, command):
    """
    Executes a PowerShell command remotely via WinRM.
    """
    #try:
    #    session = winrm.Session(WINRM_SERVER, auth=(WINRM_USERNAME, WINRM_PASSWORD))
    #    response = session.run_ps(command)

    #    if response.status_code == 0:
    #        return response.std_out.decode('utf-8').strip()  # ✅ Success
    #    else:
    #        return f"Error: {response.std_err.decode('utf-8').strip()}"  # ✅ Error handling
    #except Exception as e:
    #    log_command(narrative_id, user_profile, command, error_message)
    #    return f"WinRM Error: {str(e)}"

    # Log the command execution
    narrative_id = 1
    user_profile = "user1"
    output = "Output of the command"
    log_command(narrative_id, user_profile, command, output)
    
    return "WinRM not implemented yet"
import random

def generate_commands(narrative):
    """
    Generates PowerShell commands based on the narrative.
    """
    predefined_commands = [
        "Get-Process",
        "Get-Service",
        "Get-WmiObject Win32_ComputerSystem",
        "Get-NetIPAddress",
        "Get-EventLog -LogName Security -Newest 10"
    ]

    # Simulate dynamic command generation based on the narrative
    generated_commands = random.sample(predefined_commands, 3)
    return generated_commands

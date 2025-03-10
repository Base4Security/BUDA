Configuration
=============

Overview
--------
The BUDA framework can be finely tuned through configuration settings that govern how the system behaves in different environments. These settings allow you to customize global parameters, narrative rules, user profiles, simulated activities, and contextual information. Proper configuration ensures that BUDA’s deception operations align with your specific security requirements and operational environment.

Configuration Files and Environment Variables
-----------------------------------------------
BUDA supports configuration via files (e.g., YAML or Python settings files) and environment variables. Key configuration areas include:

- **Global Settings:**  
  General application parameters such as logging levels, database connections, and default operational parameters.

- **Narrative Settings:**  
  Rules and parameters that define the behavior of deception narratives. This includes setting the similarity threshold for activities, defining temporal limits, and specifying the duration of narrative execution.

- **User Profile Options:**  
  Parameters to customize the simulated user identities. These settings include default roles, work hours, and variability in behavior to ensure realistic interactions.

- **Activity Simulation Settings:**  
  Controls for scheduling and executing simulated activities, including the frequency of actions and the degree of randomness applied to avoid predictable patterns.

- **Contextual Parameters:**  
  Definitions that describe the operational environment, such as critical assets and threat landscape details.

Example Configuration File
--------------------------
Below is a sample snippet from a configuration file (e.g., `config.yaml`):

```yaml
# Global configuration for BUDA
global:
  log_level: INFO
  db_uri: "sqlite:///buda.db"

narrative:
  similarity_threshold: 80
  default_duration: "2h"
  temporal_limits:
    start_time: "08:00"
    end_time: "18:00"

user_profiles:
  default_role: "Analyst"
  work_hours:
    start: "09:00"
    end: "17:00"
  variability_margin: 10

activities:
  schedule_interval: "15m"
  randomness: 0.2

context:
  environment: "production"
  critical_assets: ["server1", "server2", "database1"]

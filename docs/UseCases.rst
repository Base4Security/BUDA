Use Cases
=========

This section describes some of the primary use cases that illustrate how BUDA can be applied in operational settings.

1. Attack Diversion and Early Detection
-----------------------------------------
BUDA generates realistic activity traces through simulated user profiles deployed on production workstations. This will cause adversaries interacting with internal systems to view decoy users as realistic, rather than targeting productive assets. Key benefits include:

- **Early Detection:** As attackers engage with traps, security teams can identify and alert on anomalous behaviors sooner.
- **Resource Diversion:** Adversaries are led away from genuine information, reducing the likelihood of damage to vital infrastructure.

2. Monitoring System Calibration and Validation
-------------------------------------------------
By simulating human-like interactions, BUDA could be used to validate and calibrate monitoring solutions based on user behavior (e.g., SIEM and UEBA). Using the "percentage of similarity" is possible to simulate **normal** behaviors or **anomalous** behaviors. This use case focuses on:

- **Parameter Tuning:** Automated simulation of user behavior allows for fine-tuning detection thresholds and reducing false positives.
- **Performance Benchmarking:** Continuous, realistic activity logs offer a basis for testing the sensitivity and accuracy of monitoring systems under varied scenarios.

3. Refinement of Cyber Deception Tactics
-----------------------------------------
BUDA serves as an experimental platform to refine and optimize deception strategies. Its dynamic generation of user profiles and activity patterns enables:

- **Tactical Experimentation:** Security teams can test different interaction patterns and timing variations to identify the most effective deception strategies.
- **Adaptability:** By adjusting the “personality” of fake profiles on the Activity types, the tool ensures that deceptive operations remain resilient against evolving attacker methodologies.

Next Steps
---------------
- :doc:`Narratives`
- :doc:`Installation`
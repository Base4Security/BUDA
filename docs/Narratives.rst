Narratives
==========

Overview
--------
In the BUDA framework, narratives are the backbone of every deception operation. They provide the strategic context and guidelines that shape the behavior of simulated user profiles and decoy assets. A well-defined narrative not only guides the automated generation of activities but also helps align the simulation with real-world.

Key Components
--------------
Narrative creation in BUDA is structured around three essential elements:

1. **Narrative Creator**
   - **Identification:** Assign a unique and descriptive name to the narrative.
   - **Objectives:** Define clear operational goals (e.g., diverting attacks, early detection) that guide the simulated activities.
   - **Activity Guidelines:** Set parameters (such as the percentage of similarity) to ensure the simulated behavior mirrors realistic user actions while avoiding predictability.

2. **Additional Definitions**
   - **Attacker Profile:** Specify the expected characteristics of adversaries that the narrative targets.
   - **Decoy Assets:** List and configure the fake resources (e.g., documents, network services) that will interact with the simulated profiles.
   - **Contextual Details:** Integrate information that enhances the authenticity of the scenario, making the decoys indistinguishable from genuine assets.

3. **Temporal Limits**
   - **Duration:** Establish fixed start and end times or dynamic conditions that determine how long the narrative remains active.
   - **Scheduling:** Define time-based triggers to start or stop specific activities within the narrative, ensuring the simulation reflects realistic daily routines.

Creating a Narrative
--------------------
To set up a narrative in BUDA, follow these steps:

- **Step 1: Define the Scenario**  
  Identify the operational objectives. For example, if the goal is to divert an attacker’s focus from critical systems, design the narrative to simulate routine interactions with a non-critical service.

- **Step 2: Configure Narrative Details**  
  Use the narrative creator to set:
  
  - **Name:** A clear, descriptive title.
  - **Objectives:** Goals such as early detection or attack diversion.
  - **Activity Parameters:** Guidelines that determine the percentage of simulated behavior that should mimic real user activity, allowing for controlled randomness.

- **Step 3: Integrate with Decoy Assets and User Profiles**  
  Associate the narrative with specific decoy assets and simulated user profiles to reinforce the deception. This integration ensures that every component of the simulation works in unison.

- **Step 4: Set Temporal Boundaries**  
  Define the timeframe for the narrative’s activation. This can be a fixed period (e.g., a specific date range) or conditioned upon certain operational triggers.

Placeholder for Screenshots
----------------------------
.. image:: /path/to/your/narrative_screenshot_placeholder.png
   :alt: Screenshot of the Narrative Creation Interface
   :align: center
   :width: 80%

*Note: Replace the placeholder path with the actual path to your screenshots once they are available.*

Conclusion
----------
Narratives in BUDA are designed to provide a robust and dynamic framework for simulating human-like interactions in decoy environments. By carefully designing and managing narratives, security teams can ensure that deception operations are both realistic and effective, ultimately enhancing the overall resilience against sophisticated cyber threats.

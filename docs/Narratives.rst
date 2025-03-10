Narratives
==========

Overview
--------
In BUDA framework, narratives are the backbone of every deception operation. They provide the strategic context and guidelines that shape the behavior of simulated user profiles and decoy assets. A well-defined narrative not only guides the automated generation of activities but also helps align the simulation with real-world.

Key Components
--------------
Narrative creation in BUDA is structured around three essential elements:

1. **Narrative definitions**

   - **Title:** Assign a unique and descriptive name to the narrative.

   - **Objective:** Define clear operational goals (e.g., diverting attacks, early detection) that guide the simulated activities.

   - **Assigned User Profiles:** Specify the simulated user profiles that will participate in the narrative.

2. **Additional elemets**

   - **Attacker Profile:** Specify the expected characteristics of adversaries that the narrative targets.

   - **Deception Activities:** List and configure the fake resources (e.g., documents, network services) that will interact with the simulated profiles.

   - ** Similarity Threshold:** Set the percentage of simulated behavior that should mimic real user activity.

3. **Temporal limit**

   - **End Date:** Set a deadline for the narrative to conclude.

Creating a Narrative
--------------------
To set up a narrative in BUDA, follow these steps:

- **Step 1: Prepare the Scenario**  
  Identify the operational objectives. For example, if the goal is to divert an attacker’s focus from critical systems, design the narrative to simulate routine interactions with a non-critical service.

- **Step 2: Configure Narrative Details**  
  Use the Narratives menu to set the configuration paramenters.

.. image:: /images/narratives/narrative_creation_interface.png
   :alt: Screenshot of the Narrative Creation Interface
   :align: center
   :width: 80%

  Use the LLMs to assist in the narrative creation process. The LLMs can provide insights on the narrative design to enhance the strategy.

.. image:: /images/narratives/narrative_creation_assisted.png
   :alt: Screenshot of the Narrative Creation with LLMs assistance
   :align: center
   :width: 80%

- **Step 3: Review the created narrative**
  Review the narrative to ensure that all the necessary components are included and configured correctly.

.. image:: /images/narratives/narrative_review_buttton.png
   :alt: Screenshot of the Narrative Review Button
   :align: center
   :width: 80%

.. image:: /images/narratives/narrative_review_interface.png
   :alt: Screenshot of the Narrative Review Interface
   :align: center
   :width: 80%

.. note::
   Narratives can be modified at any time to adapt to changing operational requirements. By carefully designing narratives, security teams can ensure that deception operations are effective, ultimately enhancing the overall resilience against sophisticated cyber threats.

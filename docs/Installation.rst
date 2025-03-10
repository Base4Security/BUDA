Installation
============

Overview
--------
This section guides you through installing the BUDA framework (Behavioral User-driven Deceptive Activities Framework) on your system. Follow the steps below to set up your environment, install dependencies, and verify that BUDA is ready to use.

Requirements
------------
- **Python 3.7+**: Ensure that Python is installed on your system.
- **pip**: Make sure you have an updated version of pip.
- **Virtual Environment (Recommended)**: To avoid dependency conflicts, use a virtual environment.

Installation Steps
------------------
1. **Clone the Repository (if installing from source)**
   
   Open your terminal or Command Prompt and run:
   
   ``
   git clone https://github.com/Base4Security/BUDA.git
   ``
   ``
   cd BUDA
   ``

2. **Create a Virtual Environment (Optional)**
   
   If you plan to use BUDA in a production environment, it is recommended to create a virtual environment to isolate dependencies and avoid conflicts. To create a virtual environment, run:
   
   ``
   python -m venv venv
   ``
   
   Activate the virtual environment:
   
   ``
   source venv/bin/activate
   ``

3. **Install BUDA Package**
   
   Install the BUDA package using pip:
   
   ``
   pip install .
   ``
4. **Verify Installation**
   
   To verify that BUDA is installed correctly, run:
   
   ``
   python -c "import BUDA;"
   ``

   ``
   buda --version
   ``
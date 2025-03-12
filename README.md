<p align="center">
	<a href="https://budaframework.readthedocs.io/en/latest/" rel="noopener">
	 	<img src="https://github.com/Base4Security/BUDA/blob/35615ab92d4f484e8ed812d86f2f000e68d4aaf4/docs/images/logo.png?raw=true" alt="BUDA">
	</a>
</p>

<h2 align="center">BUDA</h2>
<h3 align="center"><i>Behavioral User-driven Deceptive Activities</i></h2>

<hr>
<div align="center">
<br>

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-GPL-blue.svg)](/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/buda/badge/?version=latest)](https://budaframework.readthedocs.io/en/latest/?badge=latest)

</div>

<div align="center">

[![GitHub release](https://img.shields.io/github/release/Base4Security/BUDA.svg)](https://GitHub.com/Base4Security/BUDA/releases/)
[![GitHub issues](https://img.shields.io/github/issues/Base4Security/BUDA.svg)](https://GitHub.com/Base4Security/BUDA/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/Base4Security/BUDA.svg)](https://GitHub.com/Base4Security/BUDA/pull/)

</div>

## About

BUDA is a **cutting-edge experimental cybersecurity solution** designed to **automate the simulation of realistic user behaviors** within **decoy environments**.  

By integrating:  
✅ **Strategic narratives**  
✅ **Dynamic user profiles**  
✅ **Automated activity simulation**  

BUDA models **credible decoys** that **mislead attackers** and **strengthen defense mechanisms**.  

It **recreates normal activity patterns** in your environment, enhancing **deception strategies** through the **generation of automated and realistic digital footprints**. 

---

## 🚀 Features
- **Extract context from Windows EVTX Logs**  
- **Narrative Management**  
- **User Profiles Management**
- **Activity generation engine**
- **LLM Integration for Assisted Generation**
- **Narrative-Driven Deception**

---

## 📖 Table of Contents

- [🛠️ Installation & Setup](#️-installation--setup)
- [🔥 How It Works](#-how-it-works)
- [🤝 Contributing](#-contributing)

---

## 🛠️ Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Base4Security/BUDA.git
cd BUDA
```

### **2️⃣ Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install the BUDA package**
```bash
pip install .
```

### **4️⃣ Verify the installation**
```bash
python -c "import BUDA;"
buda --version
```

### **5️⃣ Start BUDA**
```bash
python run.py
```

Now, visit **`http://127.0.0.1:9875/`** in your browser and enjoy!

---

## 🔥 How It Works

BUDA operates by simulating realistic user behaviors within a **decoy environment** to enhance cyber deception strategies. It achieves this through the orchestration of several key components working in concert.  

### 🛠 Process Breakdown  

#### 📌 Context Integration  
The process begins by integrating real-world environmental data into BUDA through the **Global Context**. This involves uploading **EVTX logs** to extract information such as:  
- Usernames  
- IP addresses  
- Device names  

These details influence all aspects of activity creation and command execution. The **Global Context** serves as the foundation for generating realistic simulations.  

#### 📖 Narrative Definition  
Next, you define **Narratives**, which act as the **strategic backbone** of the deception operation. A **narrative** outlines:  
- **Operational goals** (e.g., diverting attacks, enabling early detection)  
- **Simulated user profiles** participating in the deception  
- **Attacker profile expectations**  
- **Deception activities** (fake resources)  

By setting a **similarity threshold**, you can control how closely the simulated behavior mimics real user activity.  

#### 👤 User Profile Creation  
With a **narrative** in place, you configure **User Profiles**, representing **simulated identities**. These profiles mimic real users by defining attributes such as:  
- Name and role  
- Behavioral patterns (work hours, application usage)  
- WinRM server details for executing activities  

Profiles can be created manually or generated with **Language Models (LLMs)**. Each profile is linked to one or more narratives, defining its role in deception operations.  

#### 🎭 Activity Simulation  
BUDA then **simulates user actions** through **Activities**, creating a credible digital footprint. Activities are defined by:  
- **Action types** (e.g., browsing, logins, file access)  
- **Action details** (e.g., target file, URL)  
- **Assigned user profiles** performing the activity  

You can manually create custom activity sequences or use **LLM-assisted generation** to design effective **deception strategies**.  

#### 🤖 LLM Assistance  
Throughout the process, BUDA leverages **Language Models (LLMs)** for realistic and contextually relevant data generation. You can configure the LLM provider (**OpenAI or LM Studio**) and the specific model in the BUDA settings.  

#### 🚀 Execution and Monitoring  
Once narratives, user profiles, and activities are configured, BUDA executes the **simulated actions**. The resulting activity traces aim to:  
- **Create a realistic but deceptive environment**  
- **Monitor interactions** with decoy elements  
- **Achieve early detection** of adversaries  
- **Divert attacker attention** from real assets  
- **Calibrate and validate monitoring systems**  

### 🔎 Summary  
BUDA **populates a believable environment** with **fake user identities** engaging in **normal-looking activities**, making it harder for attackers to distinguish between **real and decoy** systems. This approach enhances **cyber defense** by:  
✅ Providing early warnings  
✅ Diverting threats  
✅ Refining deception tactics  


---


Want to contribute? **Fork this repo & submit a PR!** 🚀



import json
import os
import re
from collections import defaultdict
from Evtx.Evtx import Evtx
from xml.etree import ElementTree

CONTEXT_FILE = "context.json"


def extract_ueba_from_evtx(evtx_path):
    """
    Extract UEBA insights from an EVTX log file.
    :param evtx_path: Path to the EVTX file
    :return: Dictionary with extracted UEBA data
    """
    usernames = set()
    work_hours = defaultdict(int)
    ip_addresses = set()
    devices = set()
    login_frequencies = defaultdict(int)

    namespace = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

    with Evtx(evtx_path) as log:
        for record in log.records():
            xml_string = record.xml()
            xml_root = ElementTree.fromstring(xml_string)

            # Extract Event ID (Windows Logon Events)
            event_id_element = xml_root.find(".//ns:EventID", namespace)
            event_id = event_id_element.text if event_id_element is not None else "Unknown"

            print('event_id:', event_id)

            # Extract user logins
            username_match = re.search(r"Account Name:\s*(\w+)", xml_string, re.IGNORECASE)
            username_element = xml_root.find(".//ns:EventData/ns:Data[@Name='SubjectUserName']", namespace)
            SubjectUserName = username_element.text if username_element is not None else None
            
            if username_match:
                username = username_match.group(1)
                usernames.add(username)
                login_frequencies[username] += 1
            
            if SubjectUserName:
                username = SubjectUserName
                usernames.add(username)
                login_frequencies[username] += 1

            # Extract login timestamps (Event ID 4624 = Logon)
            if event_id == "4624":
                time_match = re.search(r"Time Created=\"(\d{2}):(\d{2})", xml_string)
                if time_match:
                    hour = int(time_match.group(1))
                    work_hours[hour] += 1

            # Extract IP Addresses
            ip_match = re.search(r"Source Network Address:\s*(\d+\.\d+\.\d+\.\d+)", xml_string)
            if ip_match:
                ip_addresses.add(ip_match.group(1))

            # Extract Device Name
            device_match = re.search(r"Workstation Name:\s*([\w-]+)", xml_string)
            if device_match:
                devices.add(device_match.group(1))

    extracted_data = {
        "usernames": list(usernames),
        "work_hours": {str(k): v for k, v in work_hours.items()},
        "ip_addresses": list(ip_addresses),
        "devices": list(devices),
        "login_frequencies": dict(login_frequencies)
    }

    return extracted_data


def update_context_file(new_data):
    """
    Appends extracted UEBA data to context.json without duplicates.
    :param new_data: Extracted data dictionary
    """
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, 'r') as f:
                context = json.load(f)
        else:
            context = {"usernames": [], "work_hours": {}, "ip_addresses": [], "devices": [], "login_frequencies": {}}

        # Merge usernames
        context["usernames"] = list(set(context["usernames"]) | set(new_data.get("usernames", [])))

        # Merge work hours
        for hour, count in new_data.get("work_hours", {}).items():
            context["work_hours"][hour] = context["work_hours"].get(hour, 0) + count

        # Merge IP addresses
        context["ip_addresses"] = list(set(context["ip_addresses"]) | set(new_data.get("ip_addresses", [])))

        # Merge devices
        context["devices"] = list(set(context["devices"]) | set(new_data.get("devices", [])))

        # Merge login frequencies
        for user, count in new_data.get("login_frequencies", {}).items():
            context["login_frequencies"][user] = context["login_frequencies"].get(user, 0) + count

        # Save updated context
        with open(CONTEXT_FILE, 'w') as f:
            json.dump(context, f, indent=4)

        print("Context updated successfully.")

    except Exception as e:
        print(f"Error updating context.json: {e}")

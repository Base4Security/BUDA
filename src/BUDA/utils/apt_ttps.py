import csv
from BUDA import db
from ..models import APTGroups, TTPUsed

def import_aptgroups_and_ttps_from_csv(file_path):
    """
    Imports APTGroup and associated TTPUsed from a CSV file.
    :param file_path: Path to the CSV file
    """
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                apt_name = row['name'].strip()
                ttp_used = row['ttpused'].strip()

                # Find or create the APTGroup
                apt_group = APTGroups.query.filter_by(name=apt_name).first()
                if not apt_group:
                    apt_group = APTGroups(name=apt_name)
                    db.session.add(apt_group)
                    db.session.flush()  # Ensure apt_group.id is available

                # Add the TTPUsed for the APTGroup
                ttp_entry = TTPUsed.query.filter_by(aptgroup_id=apt_group.id, ttp=ttp_used).first()
                if not ttp_entry:
                    ttp_entry = TTPUsed(ttp=ttp_used, aptgroup_id=apt_group.id)
                    db.session.add(ttp_entry)

            # Commit the changes to the database
            db.session.commit()
            print("APTGroups and TTPs successfully imported.")
    except Exception as e:
        print(f"Error importing APTGroups: {e}")

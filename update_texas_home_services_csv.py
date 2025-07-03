import csv
import json

CSV_FILE = 'leads_home_services_in_texas.csv'
JSON_FILE = 'leads_home_services_in_texas.json'
OUTPUT_FILE = 'leads_home_services_in_texas.csv'  # Overwrite in place

# Load JSON data
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    leads_json = json.load(f)

# Build a lookup by normalized name
json_lookup = {lead['name'].strip().lower(): lead for lead in leads_json}

def get_field(lead, field):
    return lead.get(field, '') or ''

def get_list_field(lead, field):
    val = lead.get(field, [])
    if isinstance(val, list):
        return '; '.join([v for v in val if v])
    return val if isinstance(val, str) else ''

def get_employees_field(lead, key):
    # For employees, directors, etc. in 'employees' or 'contacts' list
    results = []
    for emp in lead.get('employees', []) + lead.get('contacts', []):
        if key == 'director_linkedins' and 'director' in (emp.get('title', '').lower()):
            if emp.get('linkedin_url'): results.append(emp['linkedin_url'])
        elif key == 'employee_linkedins' and emp.get('linkedin_url'):
            results.append(emp['linkedin_url'])
        elif key == 'verified_emails' and emp.get('verified_email'):
            results.append(emp['verified_email'])
    # Deduplicate
    return '; '.join(sorted(set([r for r in results if r])))

def get_all_employee_linkedins(lead):
    # Also check for 'employee_linkedins' field
    links = set(get_employees_field(lead, 'employee_linkedins').split('; ')) if get_employees_field(lead, 'employee_linkedins') else set()
    if 'employee_linkedins' in lead:
        links.update([l for l in lead['employee_linkedins'] if l])
    return '; '.join(sorted([l for l in links if l]))

def get_all_director_linkedins(lead):
    return get_employees_field(lead, 'director_linkedins')

def get_all_verified_emails(lead):
    emails = set(get_employees_field(lead, 'verified_emails').split('; ')) if get_employees_field(lead, 'verified_emails') else set()
    return '; '.join(sorted([e for e in emails if e]))

def update_csv():
    with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
        fieldnames = reader[0].keys()

    # Add new columns if not present
    new_columns = [
        'ceo_linkedin', 'owner_linkedin', 'manager_linkedin',
        'director_linkedins', 'employee_linkedins', 'verified_emails'
    ]
    fieldnames = list(fieldnames)
    for col in new_columns:
        if col not in fieldnames:
            fieldnames.append(col)

    updated_rows = []
    for row in reader:
        name = row['name'].strip().lower()
        lead = json_lookup.get(name)
        if lead:
            row['ceo_linkedin'] = get_field(lead, 'ceo_linkedin')
            row['owner_linkedin'] = get_field(lead, 'owner_linkedin')
            row['manager_linkedin'] = get_field(lead, 'manager_linkedin')
            row['director_linkedins'] = get_all_director_linkedins(lead)
            row['employee_linkedins'] = get_all_employee_linkedins(lead)
            row['verified_emails'] = get_all_verified_emails(lead)
        else:
            for col in new_columns:
                row[col] = ''
        updated_rows.append(row)

    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

if __name__ == '__main__':
    update_csv() 
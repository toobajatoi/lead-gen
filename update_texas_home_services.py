import json
import re

# Read the existing JSON file
with open('leads_home_services_in_texas.json', 'r', encoding='utf-8') as file:
    existing_data = json.load(file)

# New data to add (consolidated from all the arrays provided)
new_data = [
    {
        "name": "All Texas Home Services & Remodeling",
        "linkedin_ceo_or_owner": "https://www.linkedin.com/in/mike-issa-4a9abb139",
        "linkedin_directors": [],
        "verified_emails": []
    },
    {
        "name": "North Texas Home Care",
        "linkedin_company": "https://www.linkedin.com/company/north-texas-therapy-and-home-care",
        "linkedin_employees": [
            "https://www.linkedin.com/in/louise-walsh-8b7b1649",
            "https://www.linkedin.com/in/lori-rice-7b398315b",
            "https://www.linkedin.com/in/amy-karlin-86b989a2",
            "https://www.linkedin.com/in/sherry-calder-306050328"
        ],
        "verified_emails": ["info@northtexastherapy.com"]
    },
    {
        "name": "A-Plus Air Conditioning & Home Solutions",
        "linkedin_company": "https://www.linkedin.com/company/a-plus-energy-management-air-conditioning-%26-home-solutions",
        "linkedin_ceo": "https://www.linkedin.com/in/greg-yamin-a226a113",
        "linkedin_manager": "https://www.linkedin.com/in/josh-yamin-5967598a",
        "verified_emails": []
    },
    {
        "name": "Lane Service",
        "linkedin_owner": "https://www.linkedin.com/in/jimmy-lane-84299b41",
        "verified_emails": ["laneservices@hot.rr.com"]
    },
    {
        "name": "Mobile Home Repairs of Texas",
        "linkedin_owner": "https://www.linkedin.com/in/gerald-loden-1130a0b6",
        "verified_emails": ["medic4043@gmail.com"]
    },
    {
        "name": "My Texas Home Services",
        "linkedin_owner": "https://www.linkedin.com/in/len-waatti-705878163",
        "linkedin_employee": "https://www.linkedin.com/in/sean-briggs-76401723",
        "verified_emails": ["contact@mytexashomeservicesdfw.com"]
    },
    {
        "name": "Texas Maintenance Pros",
        "linkedin_company": "https://www.linkedin.com/in/texas-maintenance-pros-806b0227a",
        "verified_emails": []
    },
    {
        "name": "Texas Tough Home Services",
        "linkedin_owner": "https://www.linkedin.com/in/ross-icet-8b402344",
        "verified_emails": []
    },
    {
        "name": "RedHome HVAC Services",
        "linkedin_company": "https://www.linkedin.com/company/redhome-io",
        "employees": [
            {
                "name": "Elton Stewart",
                "title": "Co‑Founder",
                "linkedin_url": "https://www.linkedin.com/in/elton-stewart-ab1a032a",
                "email": None
            }
        ],
        "verified_emails": []
    },
    {
        "name": "United States Home Services",
        "linkedin_company": "https://www.linkedin.com/company/united-states-home-services",
        "verified_emails": []
    },
    {
        "name": "Texas Home Remodel & Repair",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["info@txhomeremodelrepair.com"]
    },
    {
        "name": "Home Care Senior Services, Inc",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["sally@homecareseniorservices.com"]
    },
    {
        "name": "Milestone Electric, A/C, & Plumbing",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["media@callmilestone.com", "contact-us@callmilestone.com"]
    },
    {
        "name": "Austin's Home Services LLC",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": []
    },
    {
        "name": "Central Home Health Services of Tx",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": []
    },
    {
        "name": "AGES Services Company",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["Dispatch@agesservco.com"]
    },
    {
        "name": "A Home Services",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": []
    },
    {
        "name": "Texas Total Home Services",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["sales@texastotalhomeservices.com"]
    },
    {
        "name": "Home Service Specialist Inc",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": []
    },
    {
        "name": "Texas Home Care Partners",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": []
    },
    {
        "name": "Texas Home Performance | HVAC Services",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["service@texashomeperformance.com"]
    },
    {
        "name": "Daily Service Company",
        "address": "507 Sun Valley Blvd, Hewitt, TX 76643, United States",
        "phone": "+1 254-754-5250",
        "website": "https://www.dailyserviceco.com/",
        "linkedin_company_url": "",
        "employees": [
            {
                "name": "Scott (Owner)",
                "title": "Owner",
                "linkedin_url": "",
                "verified_email": ""
            },
            {
                "name": "Lisa (Co‑Owner & Accountant)",
                "title": "Co‑Owner & Accountant",
                "linkedin_url": "",
                "verified_email": ""
            }
        ],
        "verified_emails": []
    },
    {
        "name": "High Standards Home Services",
        "address": "",
        "phone": "+1 512-635-6515",
        "website": "",
        "linkedin_company_url": "",
        "employees": [
            {
                "name": "Velicity Matthews",
                "title": "Owner",
                "linkedin_url": "https://www.linkedin.com/in/velicity-matthews-659b86219",
                "verified_email": ""
            }
        ],
        "verified_emails": []
    },
    {
        "name": "OnCall Home and Commercial Services",
        "address": "9029 Research Blvd #500, Austin, TX 78758, United States",
        "phone": "+1 512-703-7302",
        "website": "http://www.oncallaustin.com/",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["info@oncallaustin.com"]
    },
    {
        "name": "Freedom Home Services",
        "address": "",
        "phone": "+1 281-748-0055",
        "website": "http://www.freedomhomeservices.com/",
        "linkedin_company_url": "https://www.linkedin.com/company/freedom-home-services-usa/",
        "employees": [],
        "verified_emails": ["info@freedomhomeservices.com"]
    },
    {
        "name": "Freedom Home Services USA",
        "category": "General contractor",
        "address": "16720 Stuebner Airline Rd, Spring, TX 77379, United States",
        "website": "http://freedomhomeservices.com/",
        "phone": "",
        "linkedin_company_url": "https://www.linkedin.com/company/freedom-home-services-usa",
        "employees": [
            {
                "name": "Maury Hammond",
                "title": "Owner / Hoarding & Renovations Expert",
                "linkedin_url": "https://www.linkedin.com/in/mauryhammond",
                "verified_email": "mauryh20@gmail.com"
            },
            {
                "name": "Sadaqat Ali",
                "title": "General Contractor",
                "linkedin_url": None,
                "verified_email": None
            }
        ]
    },
    {
        "name": "Texas Angels Home Care",
        "category": "Home health care service",
        "address": "6310 Southwest Blvd Suite 202, Fort Worth, TX 76109, United States",
        "website": "http://www.texasangelshomecare.com/index.html",
        "phone": "+1 817-727-4525",
        "linkedin_company_url": "https://www.linkedin.com/company/texas-angels-home-care",
        "employees": [
            {
                "name": "Julie Woodside",
                "title": "Owner / Manager",
                "linkedin_url": "https://www.linkedin.com/in/juliewoodside",
                "verified_email": None
            },
            {
                "name": "Lauren Vickers",
                "title": "Home Health Aide / Caregiver",
                "linkedin_url": None,
                "verified_email": None
            },
            {
                "name": "TrangD Salgado",
                "title": "Caregiver",
                "linkedin_url": None,
                "verified_email": None
            }
        ]
    },
    {
        "name": "County Wide Service Co.",
        "category": "HVAC contractor",
        "address": "5410 Jackwood Dr, San Antonio, TX 78238, United States",
        "website": "https://www.countywideservice.com/",
        "phone": "+1 210-526-0497",
        "linkedin_company_url": "https://www.linkedin.com/company/county-wide-service/",
        "employees": [
            {
                "name": "Sharon Bahamonde",
                "title": "Office Manager",
                "linkedin_url": "https://www.linkedin.com/in/sharonbahamonde/",
                "verified_email": None
            },
            {
                "name": "Mike Bahamonde",
                "title": "Owner",
                "linkedin_url": "https://www.linkedin.com/in/mikebahamonde/",
                "verified_email": None
            }
        ]
    },
    {
        "name": "911 Austin Home Services",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["Walterlukesh89@icloud.com"]
    },
    {
        "name": "Texas Superior Home Services",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["Texassuperior@outlook.com"]
    },
    {
        "name": "Your Texas Home Service LLC",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["yourtexashomeservice01@gmail.com"]
    },
    {
        "name": "A Better Home Services",
        "linkedin_company_url": "",
        "employees": [],
        "verified_emails": ["ben.sanchez@abetterhomeservices.com"]
    },
    {
        "name": "TheKey - Senior Home Care",
        "category": "Home health care service",
        "address": "3601 NE Loop 820 Ste 104, Fort Worth, TX 76137, United States",
        "website": "https://thekey.com/fort‑worth",
        "phone": "+1 682-900-2806",
        "linkedin_company_url": "https://www.linkedin.com/company/thekeycare/",
        "employees": [
            {
                "name": "Kimberly John",
                "title": "Branch Manager",
                "linkedin_url": "https://www.linkedin.com/in/kimberlyjohn/",
                "verified_email": None
            }
        ]
    },
    {
        "name": "Signature Home Services, Inc.",
        "category": "General contractor",
        "address": "1201 Hillview Dr, Keller, TX 76248, United States",
        "website": "https://www.signaturehomeservices.com/",
        "phone": "+1 817-562-9662",
        "linkedin_company_url": "https://www.linkedin.com/company/curb-appeal-renovations-inc/",
        "employees": [
            {
                "name": "David Roberts",
                "title": "Owner",
                "linkedin_url": "https://www.linkedin.com/in/davidrobertssignaturehs/",
                "verified_email": None
            }
        ]
    },
    {
        "name": "Home Care Providers of Texas",
        "category": "Home health care service",
        "address": "14114 Dallas Pkwy #530, Dallas, TX 75254, United States",
        "website": "https://www.hcpoftexas.com/",
        "phone": "+1 972-735-0801",
        "linkedin_company_url": "https://www.linkedin.com/company/74362921/",
        "employees": [
            {
                "name": "Sally Thompson",
                "title": "CEO",
                "linkedin_url": "https://www.linkedin.com/in/sallythompsonhcp/",
                "verified_email": "sally@homecareseniorservices.com"
            }
        ]
    }
]

def normalize_name(name):
    """Normalize company name for comparison"""
    return re.sub(r'[^\w\s]', '', name.lower()).strip()

def find_matching_company(new_name, existing_data):
    """Find matching company in existing data"""
    normalized_new = normalize_name(new_name)
    
    for item in existing_data:
        normalized_existing = normalize_name(item['name'])
        if normalized_new == normalized_existing:
            return item
        # Check for partial matches
        if normalized_new in normalized_existing or normalized_existing in normalized_new:
            return item
    return None

# Update existing entries and add new ones
updated_count = 0
added_count = 0

for new_item in new_data:
    new_name = new_item['name']
    existing_item = find_matching_company(new_name, existing_data)
    
    if existing_item:
        # Update existing entry
        updated_count += 1
        
        # Add LinkedIn information
        if 'linkedin_company' in new_item and new_item['linkedin_company']:
            existing_item['linkedin_company_url'] = new_item['linkedin_company']
        elif 'linkedin_company_url' in new_item and new_item['linkedin_company_url']:
            existing_item['linkedin_company_url'] = new_item['linkedin_company_url']
        
        # Add verified emails
        if 'verified_emails' in new_item and new_item['verified_emails']:
            existing_emails = set(existing_item.get('emails', []))
            new_emails = set(new_item['verified_emails'])
            existing_item['emails'] = list(existing_emails.union(new_emails))
        
        # Add employee information
        if 'employees' in new_item and new_item['employees']:
            if 'employees' not in existing_item:
                existing_item['employees'] = []
            existing_item['employees'].extend(new_item['employees'])
        
        # Add CEO/Owner information
        if 'linkedin_ceo_or_owner' in new_item and new_item['linkedin_ceo_or_owner']:
            if 'ceo_linkedin' not in existing_item:
                existing_item['ceo_linkedin'] = new_item['linkedin_ceo_or_owner']
        
        if 'linkedin_owner' in new_item and new_item['linkedin_owner']:
            if 'owner_linkedin' not in existing_item:
                existing_item['owner_linkedin'] = new_item['linkedin_owner']
        
        # Add other LinkedIn information
        if 'linkedin_ceo' in new_item and new_item['linkedin_ceo']:
            if 'ceo_linkedin' not in existing_item:
                existing_item['ceo_linkedin'] = new_item['linkedin_ceo']
        
        if 'linkedin_manager' in new_item and new_item['linkedin_manager']:
            if 'manager_linkedin' not in existing_item:
                existing_item['manager_linkedin'] = new_item['linkedin_manager']
        
        # Add employee LinkedIn URLs
        if 'linkedin_employees' in new_item and new_item['linkedin_employees']:
            if 'employee_linkedins' not in existing_item:
                existing_item['employee_linkedins'] = []
            existing_item['employee_linkedins'].extend(new_item['linkedin_employees'])
        
        if 'linkedin_employee' in new_item and new_item['linkedin_employee']:
            if 'employee_linkedins' not in existing_item:
                existing_item['employee_linkedins'] = []
            existing_item['employee_linkedins'].append(new_item['linkedin_employee'])
        
        # Add directors information
        if 'linkedin_directors' in new_item and new_item['linkedin_directors']:
            if 'director_linkedins' not in existing_item:
                existing_item['director_linkedins'] = []
            existing_item['director_linkedins'].extend(new_item['linkedin_directors'])
        
        # Add CEO/Directors information
        if 'ceo_or_directors' in new_item and new_item['ceo_or_directors']:
            if 'ceo_or_directors' not in existing_item:
                existing_item['ceo_or_directors'] = []
            existing_item['ceo_or_directors'].extend(new_item['ceo_or_directors'])
        
        # Add verified email (singular)
        if 'verified_email' in new_item and new_item['verified_email']:
            if 'emails' not in existing_item:
                existing_item['emails'] = []
            if new_item['verified_email'] not in existing_item['emails']:
                existing_item['emails'].append(new_item['verified_email'])
        
        # Update other fields if they exist in new data
        for field in ['address', 'phone', 'website', 'category']:
            if field in new_item and new_item[field] and (field not in existing_item or not existing_item[field]):
                existing_item[field] = new_item[field]
    
    else:
        # Add new entry
        added_count += 1
        new_entry = {
            "name": new_item['name'],
            "rating": "",
            "reviews": "",
            "category": new_item.get('category', 'Home services'),
            "address": new_item.get('address', ''),
            "website": new_item.get('website', ''),
            "phone": new_item.get('phone', ''),
            "emails": new_item.get('verified_emails', []),
            "contacts": [],
            "linkedin_company_url": new_item.get('linkedin_company_url', '') or new_item.get('linkedin_company', ''),
            "facebook_url": "",
            "instagram_url": "",
            "twitter_url": "",
            "google_maps_url": ""
        }
        
        # Add employee information
        if 'employees' in new_item and new_item['employees']:
            new_entry['employees'] = new_item['employees']
        
        # Add CEO/Directors information
        if 'ceo_or_directors' in new_item and new_item['ceo_or_directors']:
            new_entry['ceo_or_directors'] = new_item['ceo_or_directors']
        
        # Add LinkedIn information
        if 'linkedin_ceo_or_owner' in new_item and new_item['linkedin_ceo_or_owner']:
            new_entry['ceo_linkedin'] = new_item['linkedin_ceo_or_owner']
        
        if 'linkedin_owner' in new_item and new_item['linkedin_owner']:
            new_entry['owner_linkedin'] = new_item['linkedin_owner']
        
        if 'linkedin_ceo' in new_item and new_item['linkedin_ceo']:
            new_entry['ceo_linkedin'] = new_item['linkedin_ceo']
        
        if 'linkedin_manager' in new_item and new_item['linkedin_manager']:
            new_entry['manager_linkedin'] = new_item['linkedin_manager']
        
        if 'linkedin_employees' in new_item and new_item['linkedin_employees']:
            new_entry['employee_linkedins'] = new_item['linkedin_employees']
        
        if 'linkedin_employee' in new_item and new_item['linkedin_employee']:
            new_entry['employee_linkedins'] = [new_item['linkedin_employee']]
        
        if 'linkedin_directors' in new_item and new_item['linkedin_directors']:
            new_entry['director_linkedins'] = new_item['linkedin_directors']
        
        # Add verified email (singular)
        if 'verified_email' in new_item and new_item['verified_email']:
            if isinstance(new_item['verified_email'], list):
                new_entry['emails'] = new_item['verified_email']
            else:
                new_entry['emails'] = [new_item['verified_email']] if new_item['verified_email'] else []
        
        existing_data.append(new_entry)

# Write the updated JSON file
with open('leads_home_services_in_texas.json', 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, indent=4, ensure_ascii=False)

print(f"Update completed!")
print(f"Updated {updated_count} existing entries")
print(f"Added {added_count} new entries")
print(f"Total entries: {len(existing_data)}") 
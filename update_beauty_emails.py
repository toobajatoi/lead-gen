import json

# Read the existing JSON file
with open('leads_beauty_shops_in_new_york.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Email data to add (from user's provided data)
email_updates = {
    "Estilismo Beauty Salon": None,  # No email provided
    "Beauty Life Hair Color Studio": None,  # No email provided
    "V one Beauty": None,  # No email provided
    "Maison de MI Salon | Korean Hair Salon": None,  # No email provided
    "Wanda's Beauty Salon": None,  # No email provided
    "AATE BEAUTY SALON": None,  # No email provided
    "DeCode Salon": None,  # No email provided
    "Hair Decor NYC Salon": "hairdecorunisex@gmail.com",  # Already exists
    "Dolores Beauty Salon": None,  # No email provided
    "Agape Beauty Salon": "agapesalon1@gmail.com",  # Already exists
    "Fabio's Hair & Color Studio": "fabiohairstudio@hotmail.com",
    "Rogue House Salon": None,  # No email provided
    "Bloom Beauty Lounge": None,  # No email provided
    "The House of Beauty NYC": "thehouseofbeautynyc@gmail.com",
    "New York Beauty Center": None,  # No email provided
    "Clean By Crystal": None,  # No email provided
    "Color Vue Hair Lounge": None,  # No email provided
    "Glamsquad": None,  # No email provided
    "Toka Salon": "tokaguestservices@gmail.com",
    "Marie Robinson salon": "marierobinsonsalon@gmail.com",
    "Jolieden's Beauty Bar": "marketing@joliedensbeautybar.com",
    "Elore Beauty Space": "hello@elorebeautyspace.com",
    "Athena's Beauty": "athenasbeauty@aol.com",
    "Aube Beauty Salon NYC": None,  # No email provided
    "Salon Jatel": "337-9600SALONJATEL@GMAIL.COM",
    "U&I Spa - Laser, Eyelashes & Facials Beauty Salon": "uandispa@gmail.com",
    "Michi Beauty Salon": "salonmichiny@gmail.com",
    "Ollin Salon NYC": None,  # No email provided
    "SHAIR UNION SQUARE Hair Salon": None,  # No email provided
    "Shampoo Avenue B": None,  # No email provided
    "Empire Beauty School": "officeofpresident@empire.edu",
    "Salons by JC - Luxury hair, beauty, wellness & salon suites in NYC 59th St": "contact@salonsbyjc.com",
    "Citryne Rose New York": "info@citrynerosenewyork.com",
    "Mode Beauty NYC": "heather@modebeautynyc.com",
    "WS HAIRSTYLING NYC": None,  # No email provided
    "Honeybliss Salon": "info@honeyblisssalon.com",
    "New Ocean Salon": None,  # No email provided
    "Hair Bar NYC Midtown": None,  # No email provided
    "Sunny City Beauty Salon (名发城）": None,  # No email provided
    "Yukie Natori New York Salon & Spa": None,  # No email provided
    "Mure Salon": None,  # No email provided
    "Beauty Supply": None,  # No email provided
    "The Beauty Cave": None,  # No email provided
    "Eve Beauty Source Union Square": None,  # No email provided
    "Salon West": "salonwest85@gmail.com",
    "Arte Salon Inc": None,  # No email provided
    "Naked Beauty New York": None,  # No email provided
    "Timothy John's Salon NYC": None,  # No email provided
    "Maria Cortes NY | Hair Salon": None,  # No email provided
    "The Beauty Bar Soho": None,  # No email provided
    "Nordstrom Beauty Haven NYC": None,  # No email provided
    "Salon MUSA / Hair & Nail": None,  # No email provided
    "Wonderland Beauty Parlor": None,  # No email provided
    "The Clean Beauty Lab": "hello@thecleanbeautylab.com",
    "23rd Street Hair Salon": None,  # No email provided
    "WB Day Spa": "wbspa32st@gmail.com",
    "Mott Nyc": None,  # No email provided
    "B's Beauty Salon": None,  # No email provided
    "SAVONA Hair Beauty salon": None,  # No email provided
    "New China Beauty Salon": None,  # No email provided
    "Heavenly Light Beauty Salon by NIlda": None,  # No email provided
    "Lida's Beauty Lounge": None,  # No email provided
    "HAIRFLOW SALON BY XIOMY DOMINICAN HAIR SALON NYC": "xiomyshair@gmail.com",
    "D'Colores Beauty Salon": None,  # No email provided
    "MANHATTAN UNISEX": None,  # No email provided
    "New York Beauty Salon": None,  # No email provided
    "Shear Bliss NYC Salon": "shearblissnyc@yahoo.com",
    "Salon V": "info@salonvnyc.com",
    "Marysia Beauty Salon": None,  # No email provided
    "Adel Atelier Salon": None,  # No email provided
    "American Beauty Salons": None,  # No email provided
    "One Salon": None,  # No email provided
    "Le Salon NYC": None,  # No email provided
    "Beauty World NYC": "beautyworldlk@aol.com",
    "Lee Ren Beauty Salon": None,  # No email provided
    "Team Star Beauty Salon": None,  # No email provided
    "Luna Lucci Hair Salon": "lunalucciusa@gmail.com",
    "Catalia Beauty & Wellness": "catalianyc@gmail.com",
    "New City One Salon": None,  # No email provided
    "Krome NYC Barber Shop & Beauty Salon": None,  # No email provided
    "GS Blow Dry Bar Midtown New York City": None,  # No email provided
    "E&D Beauty Salon": None,  # No email provided
    "Sam Brocato Salon": None,  # No email provided
    "Manhattan Beauty": None,  # No email provided
    "Shine Beauty NYC": None,  # No email provided
    "NappStar NYC": None,  # No email provided
    "Federico Salon & Spa": "info@federicosalon.com",
    "Conditional Beauty Salon": None,  # No email provided
    "Bon Bon Salon": None,  # No email provided
    "Dominican Star Beauty Salon": None,  # No email provided
    "Poiz Beauty Salon": "poizbeautysalon@gmail.com",
    "Christo Fifth Avenue - Curly Hair Salon NYC": "info@christonyc.com",
    "Bon Bon Salon & Spa": None,  # No email provided
    "Perfection Beauty Salon": None,  # No email provided
    "Belkis Beauty Salon": "belkisbeautysaloncorp@gmail.com",
    "Zhu's Beauty salon": None,  # No email provided
    "Fox and Jane": "info@foxandjanesalon.com",
    "Queens Beauty Parlor": "jana@queensbeautyparlor.com"
}

# Update the data
updated_count = 0
for business in data:
    business_name = business.get("name", "")
    if business_name in email_updates:
        new_email = email_updates[business_name]
        if new_email is not None:
            # Check if emails array exists and add the email if it's not already there
            if "emails" not in business:
                business["emails"] = []
            
            if new_email not in business["emails"]:
                business["emails"].append(new_email)
                updated_count += 1
                print(f"Added email '{new_email}' to '{business_name}'")

print(f"\nTotal businesses updated: {updated_count}")

# Write the updated data back to the file
with open('leads_beauty_shops_in_new_york.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("File updated successfully!") 
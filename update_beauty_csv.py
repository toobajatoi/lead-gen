import csv

# Email updates from user (business name to email mapping)
email_updates = {
    "Estilismo Beauty Salon": None,
    "Beauty Life Hair Color Studio": None,
    "V one Beauty": None,
    "Maison de MI Salon | Korean Hair Salon": None,
    "Wanda's Beauty Salon": None,
    "AATE BEAUTY SALON": None,
    "DeCode Salon": None,
    "Hair Decor NYC Salon": "hairdecorunisex@gmail.com",
    "Dolores Beauty Salon": None,
    "Agape Beauty Salon": "agapesalon1@gmail.com",
    "Fabio's Hair & Color Studio": "fabiohairstudio@hotmail.com",
    "Rogue House Salon": None,
    "Bloom Beauty Lounge": None,
    "The House of Beauty NYC": "thehouseofbeautynyc@gmail.com",
    "New York Beauty Center": None,
    "Clean By Crystal": None,
    "Color Vue Hair Lounge": None,
    "Glamsquad": None,
    "Toka Salon": "tokaguestservices@gmail.com",
    "Marie Robinson salon": "marierobinsonsalon@gmail.com, info@marierobinsonsalon.com",
    "Jolieden's Beauty Bar": "marketing@joliedensbeautybar.com, support@joliedensbeautybar.com, customerservice@joliedensbeautybar.com",
    "Elore Beauty Space": "hello@elorebeautyspace.com",
    "Athena's Beauty": "athenasbeauty@aol.com",
    "Aube Beauty Salon NYC": None,
    "Salon Jatel": "337-9600SALONJATEL@GMAIL.COM",
    "U&I Spa - Laser, Eyelashes & Facials Beauty Salon": "uandispa@gmail.com",
    "Michi Beauty Salon": "salonmichiny@gmail.com",
    "Ollin Salon NYC": None,
    "SHAIR UNION SQUARE Hair Salon": None,
    "Shampoo Avenue B": None,
    "Empire Beauty School": "officeofpresident@empire.edu",
    "Salons by JC - Luxury hair, beauty, wellness & salon suites in NYC 59th St": "contact@salonsbyjc.com",
    "Citryne Rose New York": "info@citrynerosenewyork.com",
    "Mode Beauty NYC": "heather@modebeautynyc.com, info@modebeautynyc.com",
    "WS HAIRSTYLING NYC": None,
    "Honeybliss Salon": "info@honeyblisssalon.com",
    "New Ocean Salon": None,
    "Hair Bar NYC Midtown": None,
    "Sunny City Beauty Salon (名发城）": None,
    "Yukie Natori New York Salon & Spa": None,
    "Mure Salon": None,
    "Beauty Supply": None,
    "The Beauty Cave": None,
    "Eve Beauty Source Union Square": None,
    "Salon West": "salonwest85@gmail.com",
    "Arte Salon Inc": None,
    "Naked Beauty New York": None,
    "Timothy John's Salon NYC": None,
    "Maria Cortes NY | Hair Salon": None,
    "The Beauty Bar Soho": None,
    "Nordstrom Beauty Haven NYC": None,
    "Salon MUSA / Hair & Nail": None,
    "Wonderland Beauty Parlor": None,
    "The Clean Beauty Lab": "hello@thecleanbeautylab.com",
    "23rd Street Hair Salon": None,
    "WB Day Spa": "wbspa32st@gmail.com",
    "Mott Nyc": None,
    "B's Beauty Salon": None,
    "SAVONA Hair Beauty salon": None,
    "New China Beauty Salon": None,
    "Heavenly Light Beauty Salon by NIlda": None,
    "Lida's Beauty Lounge": None,
    "HAIRFLOW SALON BY XIOMY DOMINICAN HAIR SALON NYC": "xiomyshair@gmail.com",
    "D'Colores Beauty Salon": None,
    "MANHATTAN UNISEX": None,
    "New York Beauty Salon": None,
    "Shear Bliss NYC Salon": "shearblissnyc@yahoo.com",
    "Salon V": "info@salonvnyc.com",
    "Marysia Beauty Salon": None,
    "Adel Atelier Salon": None,
    "American Beauty Salons": None,
    "One Salon": None,
    "Le Salon NYC": None,
    "Beauty World NYC": "beautyworldlk@aol.com",
    "Lee Ren Beauty Salon": None,
    "Team Star Beauty Salon": None,
    "Luna Lucci Hair Salon": "lunalucciusa@gmail.com",
    "Catalia Beauty & Wellness": "catalianyc@gmail.com",
    "New City One Salon": None,
    "Krome NYC Barber Shop & Beauty Salon": None,
    "GS Blow Dry Bar Midtown New York City": None,
    "E&D Beauty Salon": None,
    "Sam Brocato Salon": None,
    "Manhattan Beauty": None,
    "Shine Beauty NYC": None,
    "NappStar NYC": None,
    "Federico Salon & Spa": "info@federicosalon.com",
    "Conditional Beauty Salon": None,
    "Bon Bon Salon": None,
    "Dominican Star Beauty Salon": None,
    "Poiz Beauty Salon": "poizbeautysalon@gmail.com",
    "Christo Fifth Avenue - Curly Hair Salon NYC": "info@christonyc.com",
    "Bon Bon Salon & Spa": None,
    "Perfection Beauty Salon": None,
    "Belkis Beauty Salon": "belkisbeautysaloncorp@gmail.com",
    "Zhu's Beauty salon": None,
    "Fox and Jane": "info@foxandjanesalon.com, INFO@FOXANDJANESALON.COM",
    "Queens Beauty Parlor": "jana@queensbeautyparlor.com"
}

# Read the CSV
with open('leads_beauty_shops_in_new_york.csv', 'r', encoding='utf-8') as infile:
    reader = list(csv.DictReader(infile))
    fieldnames = reader[0].keys()

# Update emails
for row in reader:
    name = row['name'].strip()
    if name in email_updates:
        email = email_updates[name]
        row['emails'] = email if email else ''

# Write the updated CSV
with open('leads_beauty_shops_in_new_york.csv', 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)

print('CSV file updated with emails in plain text format.') 
from listings import get_listings
from send_email import send_mail
from pretty_html_table import build_table

print("generating today's listings...\n")
listing_data = get_listings()
data_table = build_table(listing_data, 'blue_light')
print("drafting email...\n")
send_mail(data_table)

print("Successfully send email")
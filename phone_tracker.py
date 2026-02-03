# Import required libraries
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from opencage.geocoder import OpenCageGeocode
import folium
from api import key
import os
from dotenv import load_dotenv

load_dotenv()

# Parse the phone number
phone = phonenumbers.parse(os.getenv("PHONE_NUMBER"))
print("Parsed Phone:", phone)

# Validate the number
if not phonenumbers.is_valid_number(phone):
    print("Invalid phone number.")
    exit()

# Timezone info
time_zones = timezone.time_zones_for_geographical_number(phone)
print("Time Zones:", time_zones)

#  General region (e.g., "Kenya")
region = geocoder.description_for_number(phone, 'en')
print("Region:", region)

# Carrier info (e.g., "Safaricom")
service = carrier.name_for_number(phone, 'en')
print("Carrier:", service)

#Geocode using OpenCage
geocoder_oc = OpenCageGeocode(key)
query ="Nairobi,Kenya"
results = geocoder_oc.geocode(query)

if not results:
    print("Geocoding failed. Check your query or API key.")
    exit()

# Extract coordinates
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
print("Coordinates:", lat, lng)

# Extract county from address components
components = results[0].get('components', {})
county = components.get('county') or components.get('state_district') or "Unknown County"
print("County:", county)

#  Create map centered on location
my_map = folium.Map(location=[lat, lng], zoom_start=8)

# Add marker with county and carrier info
folium.Marker(
    [lat, lng],
    popup=f"{county} ({service})",
    tooltip="Phone Location"
).add_to(my_map)

#  Add circle for visual context
folium.Circle(
    location=[lat, lng],
    radius=5000,
    color='blue',
    fill=True,
    fill_opacity=0.2
).add_to(my_map)

#  Save map to HTML
my_map.save('python.html')
print("Map saved as APP.html")
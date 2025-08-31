# List of cities per country
Australia = ["Sydney", "Melbourne", "Brisbane", "Perth"]
UAE = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"]
India = ["Mumbai", "Bangalore", "Chennai", "Delhi"]

# Ask user for two cities
city1 = input("Enter the first city: ").strip()
city2 = input("Enter the second city: ").strip()

# Function to find country for a city
def get_country(city):
    if city in Australia:
        return "Australia"
    elif city in UAE:
        return "UAE"
    elif city in India:
        return "India"
    else:
        return None

# Get countries of both cities
country1 = get_country(city1)
country2 = get_country(city2)

# Check if both cities are in the same country
if country1 and country2:
    if country1 == country2:
        print(f"Both cities are in {country1}")
    else:
        print("They don't belong to the same country")
else:
    print("One or both cities are not in the list")

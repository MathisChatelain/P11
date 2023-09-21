import random
from uuid import uuid4
import json

min_points = 1
max_points = 20

# Generate unique random club data
clubs = []
competitions = []

while len(clubs) < 1000:  # Generate 1000 unique clubs
    clubs.append(
        {
            "name": str(uuid4()),
            "email": str(uuid4()),
            "points": str(random.randint(min_points, max_points)),
        }
    )
    competitions.append(
        {
            "name": str(uuid4()),
            "date": "2024-12-22 13:30:00",
            "numberOfPlaces": str(random.randint(min_points, max_points)),
            "places": {},
        }
    )


# Save the generated data to a JSON file
with open("mock_clubs_unique.json", "w") as json_file:
    json.dump({"clubs": clubs}, json_file, indent=4)

with open("mock_competitions_unique.json", "w") as json_file:
    json.dump({"competitions": competitions}, json_file, indent=4)

print(
    "Generated 1000 unique mock clubs and saved to 'mock_clubs_unique.json' and 1000 unique mock competitions and saved to 'mock_competitions_unique.json'"
)

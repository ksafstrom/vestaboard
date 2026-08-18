from app.vesta_strava import strava

athlete = strava.get_athlete()

print(
    f"Connected to Strava: "
    f"{athlete['firstname']} {athlete['lastname']}"
)

activity = strava.get_latest_activity()

if activity:
    print()
    print("Latest Activity")
    print("----------------")
    print(activity["name"])
    print(activity["type"])
    print(
        f"Distance: "
        f"{strava.meters_to_miles(activity['distance']):.1f} miles"
    )
    print(
        f"Elevation: "
        f"{strava.meters_to_feet(activity['total_elevation_gain']):.0f} feet"
    )
    print(
    f"Moving time: "
    f"{strava.format_duration(activity['moving_time'])}"
)
# strava.py

import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from app.common.helpers import (
    account_for_padding,
    left_align_padding,
    post_to_vestaboard,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

STRAVA_AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_URL = "https://www.strava.com/api/v3"

TOKEN_FILE = Path("tokens.json")

BOARD_WIDTH = 22
BOARD_HEIGHT = 6


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

if not STRAVA_CLIENT_ID:
    raise RuntimeError("STRAVA_CLIENT_ID is not set")

if not STRAVA_CLIENT_SECRET:
    raise RuntimeError("STRAVA_CLIENT_SECRET is not set")


# ---------------------------------------------------------
# OAuth
# ---------------------------------------------------------

def get_authorization_url(
    redirect_uri,
    scope="read,activity:read_all",
    state=None,
):
    """
    Build the Strava OAuth authorization URL.
    """

    params = {
        "client_id": STRAVA_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "approval_prompt": "auto",
        "scope": scope,
    }

    if state:
        params["state"] = state

    return f"{STRAVA_AUTHORIZE_URL}?{urlencode(params)}"


def exchange_code(code):
    """
    Exchange a Strava authorization code for access/refresh tokens.
    """

    response = requests.post(
        STRAVA_TOKEN_URL,
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
        timeout=15,
    )

    response.raise_for_status()

    tokens = response.json()

    save_tokens(tokens)

    return tokens


# ---------------------------------------------------------
# Token Storage
# ---------------------------------------------------------

def save_tokens(tokens):
    """
    Save Strava OAuth tokens locally.
    """

    TOKEN_FILE.write_text(
        json.dumps(tokens, indent=2),
        encoding="utf-8",
    )


def load_tokens():
    """
    Load stored Strava OAuth tokens.
    """

    if not TOKEN_FILE.exists():
        raise RuntimeError(
            "No Strava tokens found. "
            "Authorize the application first."
        )

    return json.loads(
        TOKEN_FILE.read_text(
            encoding="utf-8"
        )
    )


# ---------------------------------------------------------
# Token Refresh
# ---------------------------------------------------------

def refresh_access_token(refresh_token):
    """
    Refresh an expired Strava access token.
    """

    response = requests.post(
        STRAVA_TOKEN_URL,
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=15,
    )

    response.raise_for_status()

    tokens = response.json()

    save_tokens(tokens)

    return tokens


def get_valid_access_token():
    """
    Return a valid access token.

    Refreshes the token when it is within
    five minutes of expiration.
    """

    tokens = load_tokens()

    expires_at = tokens["expires_at"]

    if time.time() >= expires_at - 300:

        print("Refreshing Strava access token...")

        tokens = refresh_access_token(
            tokens["refresh_token"]
        )

    return tokens["access_token"]


# ---------------------------------------------------------
# Generic Strava API Request
# ---------------------------------------------------------

def api_request(
    method,
    endpoint,
    params=None,
):
    """
    Make an authenticated request to Strava.
    """

    access_token = get_valid_access_token()

    url = f"{STRAVA_API_URL}{endpoint}"

    response = requests.request(
        method,
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        params=params,
        timeout=15,
    )

    # Access token may have expired unexpectedly.
    if response.status_code == 401:

        print(
            "Strava returned 401. "
            "Refreshing access token..."
        )

        tokens = load_tokens()

        tokens = refresh_access_token(
            tokens["refresh_token"]
        )

        response = requests.request(
            method,
            url,
            headers={
                "Authorization":
                    f"Bearer {tokens['access_token']}",
            },
            params=params,
            timeout=15,
        )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# Athlete
# ---------------------------------------------------------

def get_athlete():
    """
    Get the authenticated Strava athlete.
    """

    return api_request(
        "GET",
        "/athlete",
    )


# ---------------------------------------------------------
# Activities
# ---------------------------------------------------------

def get_activities(
    page=1,
    per_page=30,
):
    """
    Get recent Strava activities.
    """

    return api_request(
        "GET",
        "/athlete/activities",
        params={
            "page": page,
            "per_page": min(per_page, 200),
        },
    )


def get_latest_activity():
    """
    Get the most recent Strava activity.
    """

    activities = get_activities(
        page=1,
        per_page=1,
    )

    if not activities:
        return None

    return activities[0]


def get_activity(activity_id):
    """
    Get detailed information about an activity.
    """

    return api_request(
        "GET",
        f"/activities/{activity_id}",
    )


# ---------------------------------------------------------
# Activity Filtering
# ---------------------------------------------------------

def get_activities_since(start_datetime):
    """
    Get activities since a specific datetime.
    """

    if start_datetime.tzinfo is None:
        start_datetime = start_datetime.replace(
            tzinfo=timezone.utc
        )

    start_timestamp = int(
        start_datetime.timestamp()
    )

    return api_request(
        "GET",
        "/athlete/activities",
        params={
            "after": start_timestamp,
            "page": 1,
            "per_page": 200,
        },
    )


def get_activities_this_week():
    """
    Get activities since Monday at 00:00 UTC.
    """

    now = datetime.now(timezone.utc)

    monday = now - timedelta(
        days=now.weekday()
    )

    monday = monday.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    return get_activities_since(monday)


def get_cycling_activities_this_week():
    """
    Return cycling activities from the current week.
    """

    activities = get_activities_this_week()

    cycling_types = {
        "Ride",
        "VirtualRide",
        "EBikeRide",
        "MountainBikeRide",
        "GravelRide",
    }

    return [
        activity
        for activity in activities
        if activity.get("type") in cycling_types
    ]


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

def get_weekly_cycling_stats():
    """
    Calculate cycling statistics for the current week.
    """

    activities = get_cycling_activities_this_week()

    total_distance_meters = 0
    total_elevation_meters = 0
    total_moving_seconds = 0

    for activity in activities:

        total_distance_meters += activity.get(
            "distance",
            0,
        )

        total_elevation_meters += activity.get(
            "total_elevation_gain",
            0,
        )

        total_moving_seconds += activity.get(
            "moving_time",
            0,
        )

    miles = (
        total_distance_meters / 1609.344
    )

    elevation_feet = (
        total_elevation_meters * 3.28084
    )

    moving_hours = (
        total_moving_seconds / 3600
    )

    return {
        "rides": len(activities),
        "miles": round(miles, 1),
        "elevation_feet": round(
            elevation_feet
        ),
        "moving_time_hours": round(
            moving_hours,
            1,
        ),
    }


# ---------------------------------------------------------
# Formatting
# ---------------------------------------------------------

def format_duration(seconds):
    """
    Convert seconds to H:MM:SS.
    """

    hours = seconds // 3600

    minutes = (
        (seconds % 3600) // 60
    )

    seconds = seconds % 60

    return (
        f"{hours}:{minutes:02d}:{seconds:02d}"
    )


def meters_to_miles(meters):
    """
    Convert meters to miles.
    """

    return meters / 1609.344


def meters_to_feet(meters):
    """
    Convert meters to feet.
    """

    return meters * 3.28084


# ---------------------------------------------------------
# Vestaboard - Latest Activity
# ---------------------------------------------------------

def build_latest_activity_message(activity):
    """
    Build a 6 x 22 Vestaboard message from
    a Strava activity.

    Uses helper functions for character
    conversion and padding.
    """

    if not activity:
        return [
            account_for_padding(
                "NO ACTIVITIES",
                BOARD_WIDTH,
                False,
            ),

            account_for_padding(
                "",
                BOARD_WIDTH,
                False,
            ),

            account_for_padding(
                "",
                BOARD_WIDTH,
                False,
            ),

            account_for_padding(
                "",
                BOARD_WIDTH,
                False,
            ),

            account_for_padding(
                "",
                BOARD_WIDTH,
                False,
            ),

            account_for_padding(
                "",
                BOARD_WIDTH,
                False,
            ),
        ]

    name = activity.get(
        "name",
        "LATEST RIDE",
    )

    activity_type = activity.get(
        "type",
        "ACTIVITY",
    )

    distance = meters_to_miles(
        activity.get(
            "distance",
            0,
        )
    )

    elevation = meters_to_feet(
        activity.get(
            "total_elevation_gain",
            0,
        )
    )

    moving_time = format_duration(
        activity.get(
            "moving_time",
            0,
        )
    )

    return [
        account_for_padding(
            "LATEST RIDE",
            BOARD_WIDTH,
            False,
        ),

        left_align_padding(
            name,
            BOARD_WIDTH,
        ),

        account_for_padding(
            f"{distance:.1f} MILES",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            moving_time,
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            f"{elevation:,.0f} FT",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            activity_type,
            BOARD_WIDTH,
            False,
        ),
    ]


# ---------------------------------------------------------
# Vestaboard - Weekly Stats
# ---------------------------------------------------------

def build_weekly_message():
    """
    Build a Vestaboard message showing
    cycling statistics for the current week.
    """

    stats = get_weekly_cycling_stats()

    return [
        account_for_padding(
            "THIS WEEK",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            f"{stats['rides']} RIDES",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            f"{stats['miles']:.1f} MILES",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            f"{stats['elevation_feet']:,} FT",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            f"{stats['moving_time_hours']:.1f} HOURS",
            BOARD_WIDTH,
            False,
        ),

        account_for_padding(
            "STRAVA",
            BOARD_WIDTH,
            False,
        ),
    ]


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("Starting Strava Vestaboard app...")
    print()

    print("Getting latest Strava activity...")

    activity = get_latest_activity()

    if activity:
        print(f"Activity: {activity.get('name', 'Unknown')}")
        print(f"Type: {activity.get('type', 'Unknown')}")

        distance = meters_to_miles(
            activity.get("distance", 0)
        )

        elevation = meters_to_feet(
            activity.get("total_elevation_gain", 0)
        )

        moving_time = format_duration(
            activity.get("moving_time", 0)
        )

        print(f"Distance: {distance:.1f} miles")
        print(f"Elevation: {elevation:.0f} ft")
        print(f"Moving time: {moving_time}")

    else:
        print("No Strava activities found.")

    print()
    print("Building Vestaboard message...")

    vestaboard_json_body = build_latest_activity_message(
        activity
    )

    print()
    print("Vestaboard JSON body:")

    for line in vestaboard_json_body:
        print(line)

    print()
    print("Posting to Vestaboard...")

    post_to_vestaboard(
        vestaboard_json_body
    )

    print()
    print("Vestaboard update complete.")


if __name__ == "__main__":
    main()
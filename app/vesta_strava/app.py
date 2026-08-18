import os
import secrets

from flask import (
    Flask,
    redirect,
    request,
    session,
    jsonify,
)

from dotenv import load_dotenv

from app.vesta_strava.strava import (
    get_authorization_url,
    exchange_code,
    get_athlete,
)

load_dotenv()

app = Flask(__name__)

# Flask requires a secret key to encrypt the session cookie.
app.secret_key = os.environ["FLASK_SECRET_KEY"]

REDIRECT_URI = os.environ["STRAVA_REDIRECT_URI"]


@app.route("/")
def home():
    return """
    <h1>Vestaboard Strava</h1>

    <p>
        <a href="/login">Connect Strava</a>
    </p>
    """


@app.route("/login")
def login():

    # Generate a unique OAuth state.
    state = secrets.token_urlsafe(32)

    # Store it in the Flask session.
    session["oauth_state"] = state

    # Build the Strava authorization URL.
    authorization_url = get_authorization_url(
        redirect_uri=REDIRECT_URI,
        scope="read,activity:read_all",
        state=state,
    )

    print()
    print("OAuth state generated:")
    print(state)

    print()
    print("Authorization URL:")
    print(authorization_url)

    return redirect(authorization_url)


@app.route("/callback")
def callback():

    # Values returned by Strava.
    returned_state = request.args.get("state")
    code = request.args.get("code")
    error = request.args.get("error")

    print()
    print("OAuth callback received")

    print(
        f"Returned state: {returned_state}"
    )

    print(
        f"Stored state:   {session.get('oauth_state')}"
    )

    # User denied authorization.
    if error:
        return (
            f"Strava authorization failed: {error}",
            400,
        )

    # Verify state.
    stored_state = session.get("oauth_state")

    if not stored_state:
        return (
            "No OAuth state found in Flask session. "
            "Start the authorization process again.",
            400,
        )

    if returned_state != stored_state:
        return (
            "Invalid OAuth state",
            400,
        )

    # Make sure we received a code.
    if not code:
        return (
            "No authorization code returned by Strava.",
            400,
        )

    # Exchange authorization code for tokens.
    tokens = exchange_code(code)

    # Remove state after successful authorization.
    session.pop("oauth_state", None)

    athlete = tokens.get(
        "athlete",
        {},
    )

    return jsonify({
        "status": "connected",
        "athlete": athlete.get(
            "firstname"
        ),
        "scope": tokens.get(
            "scope"
        ),
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
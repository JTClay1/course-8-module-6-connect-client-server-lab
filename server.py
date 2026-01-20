from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory list acting like a tiny database for events
# Each event is just a dict with an id and a title
events = [
    {"id": 1, "title": "Tech Meetup"},
    {"id": 2, "title": "Python Workshop"},
]

def next_event_id():
    """
    Figure out the next ID to use.
    Since this is just in-memory data, we grab the max ID and add 1.
    """
    if not events:
        return 1
    return max(event["id"] for event in events) + 1


@app.get("/")
def homepage():
    # Basic sanity-check route
    # Tests expect a JSON object with a welcome message
    return jsonify({
        "message": "Welcome to the Event Catalog API!"
    }), 200


@app.get("/events")
def get_events():
    # Return the full list of events as JSON
    # Flask will automatically convert the list of dicts
    return jsonify(events), 200


@app.post("/events")
def create_event():
    # Pull JSON data off the request
    # silent=True prevents Flask from throwing if JSON is missing
    data = request.get_json(silent=True) or {}

    # Make sure a title was actually provided
    title = data.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        # Tests accept either 400 or 422 — using 400 here
        return jsonify({
            "error": "Missing required field: title"
        }), 400

    # Build the new event object
    new_event = {
        "id": next_event_id(),
        "title": title.strip()
    }

    # Save it to our in-memory list
    events.append(new_event)

    # Return the newly created event with a 201 status
    return jsonify(new_event), 201


if __name__ == "__main__":
    # Run the server in debug mode for local development
    app.run(debug=True)

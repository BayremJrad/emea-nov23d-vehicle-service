"""Vehicle Service API — Flask implementation.

Implements the endpoints defined by the Vehicle Service - API Contract spec
and the Vehicle Service Collection:

    POST   /vehicles       Create a new vehicle
    GET    /vehicles       List all vehicles
    GET    /vehicles/<id>  Retrieve a vehicle by id
    PATCH  /vehicles/<id>  Update a vehicle by id
    DELETE /vehicles/<id>  Delete a vehicle by id

Authentication:
    All requests must send an API key in the `X-API-Key` header, matching
    the collection's API Key auth. The expected key is read from the
    API_KEY environment variable (default: "local-dev-key").
"""

import os

from flask import Flask, jsonify, request

from .models import REQUIRED_FIELDS, store

API_KEY_HEADER = "X-API-Key"
EXPECTED_API_KEY = os.environ.get("API_KEY", "local-dev-key")


def create_app():
    app = Flask(__name__)

    # ----- Auth -----------------------------------------------------------
    @app.before_request
    def require_api_key():
        # Allow the health check through without auth.
        if request.path == "/health":
            return None
        provided = request.headers.get(API_KEY_HEADER)
        if provided != EXPECTED_API_KEY:
            return jsonify({"message": "Unauthorized: missing or invalid API key."}), 401
        return None

    # ----- Health ---------------------------------------------------------
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # ----- Create ---------------------------------------------------------
    @app.post("/vehicles")
    def create_vehicle():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"message": "Request body must be a JSON object."}), 400

        # 400 - Missing required attribute
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] in (None, ""):
                return (
                    jsonify({"message": f"Request body missing required attribute: {field}"}),
                    400,
                )

        # 409 - Vehicle already exists (VIN is the natural key)
        existing = store.find_by_vin(data["vin"])
        if existing:
            return (
                jsonify(
                    {
                        "message": (
                            f"Vehicle with VIN {data['vin']} already exists. "
                            f"Existing vehicle ID: {existing['id']}"
                        )
                    }
                ),
                409,
            )

        vehicle = store.create(data)
        return jsonify(vehicle), 201

    # ----- List -----------------------------------------------------------
    @app.get("/vehicles")
    def list_vehicles():
        return jsonify(store.list()), 200

    # ----- Retrieve -------------------------------------------------------
    @app.get("/vehicles/<int:vehicle_id>")
    def get_vehicle(vehicle_id):
        vehicle = store.get(vehicle_id)
        if not vehicle:
            return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
        return jsonify(vehicle), 200

    # ----- Update ---------------------------------------------------------
    @app.patch("/vehicles/<int:vehicle_id>")
    def update_vehicle(vehicle_id):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"message": "Bad request body."}), 400

        vehicle = store.update(vehicle_id, data)
        if not vehicle:
            return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
        return jsonify(vehicle), 200

    # ----- Delete ---------------------------------------------------------
    @app.delete("/vehicles/<int:vehicle_id>")
    def delete_vehicle(vehicle_id):
        deleted = store.delete(vehicle_id)
        if not deleted:
            return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
        return "", 204

    # ----- Error handling -------------------------------------------------
    @app.errorhandler(500)
    def internal_error(_err):
        return jsonify({"message": "An unexpected error occurred."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port, debug=True)

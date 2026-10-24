
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Allow browser requests only from the configured frontend origin.
FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:8081"
)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [FRONTEND_ORIGIN]
        }
    }
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "claimsdb"),
    "user": os.getenv("DB_USER", "claimsuser"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": int(os.getenv("DB_PORT", "5432"))
}


def get_db():
    return psycopg2.connect(**DB_CONFIG)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "claims-backend"
    })


@app.route("/api/claims", methods=["GET"])
def get_claims():
    try:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, claim_number, customer_name, amount,
                           description, status, created_at
                    FROM claims
                    ORDER BY id DESC
                """)
                claims = cur.fetchall()

        return jsonify(claims)

    except psycopg2.Error:
        app.logger.exception("Database error while retrieving claims")
        return jsonify({"error": "Unable to retrieve claims"}), 500


@app.route("/api/claims", methods=["POST"])
def create_claim():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    customer_name = data.get("customer_name")
    amount = data.get("amount")
    description = data.get("description")

    if not customer_name or amount is None or amount == "":
        return jsonify({
            "error": "Customer name and amount are required"
        }), 400

    try:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO claims
                    (customer_name, amount, description)
                    VALUES (%s, %s, %s)
                    RETURNING id, claim_number, customer_name,
                              amount, description, status, created_at
                """, (customer_name, amount, description))

                claim = cur.fetchone()

        return jsonify(claim), 201

    except psycopg2.Error:
        app.logger.exception("Database error while creating a claim")
        return jsonify({"error": "Unable to create claim"}), 500


@app.route("/api/claims/<int:claim_id>", methods=["PUT"])
def update_claim(claim_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    status = data.get("status")

    if status not in ["Pending", "Approved", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    try:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    UPDATE claims
                    SET status = %s
                    WHERE id = %s
                    RETURNING id, claim_number, customer_name,
                              amount, description, status, created_at
                """, (status, claim_id))

                claim = cur.fetchone()

        if not claim:
            return jsonify({"error": "Claim not found"}), 404

        return jsonify(claim)

    except psycopg2.Error:
        app.logger.exception("Database error while updating a claim")
        return jsonify({"error": "Unable to update claim"}), 500


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    try:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                password_hash = generate_password_hash(password)

                cur.execute("""
                    INSERT INTO users
                    (name, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, email
                """, (name, email, password_hash))

                user = cur.fetchone()

        return jsonify(user), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "Email already registered"}), 409

    except psycopg2.Error:
        app.logger.exception("Database error while registering user")
        return jsonify({"error": "Unable to register user"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    try:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, name, email, password_hash
                    FROM users
                    WHERE email = %s
                """, (email,))

                user = cur.fetchone()

        if not user or not check_password_hash(
            user["password_hash"], password
        ):
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        })

    except psycopg2.Error:
        app.logger.exception("Database error while logging in")
        return jsonify({"error": "Unable to log in"}), 500


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )

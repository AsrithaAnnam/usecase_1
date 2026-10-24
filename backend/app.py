
import os

import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Allow requests from the configured frontend origin.
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

# Read database settings from environment variables.
# Defaults support running the backend directly on the host.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "claimsdb"),
    "user": os.getenv("DB_USER", "claimsuser"),
    "password": os.getenv("DB_PASSWORD", "claimspassword"),
    "port": int(os.getenv("DB_PORT", "5432")),
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
    conn = None
    cur = None

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

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

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route("/api/claims", methods=["POST"])
def create_claim():
    data = request.get_json(silent=True) or {}

    customer_name = data.get("customer_name")
    amount = data.get("amount")
    description = data.get("description")

    if not customer_name or amount is None or amount == "":
        return jsonify({
            "error": "Customer name and amount are required"
        }), 400

    conn = None
    cur = None

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            INSERT INTO claims (customer_name, amount, description)
            VALUES (%s, %s, %s)
            RETURNING id, claim_number, customer_name,
                      amount, description, status, created_at
        """, (customer_name, amount, description))

        claim = cur.fetchone()
        conn.commit()

        return jsonify(claim), 201

    except (psycopg2.Error, ValueError):
        if conn:
            conn.rollback()
        app.logger.exception("Error while creating claim")
        return jsonify({"error": "Unable to create claim"}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route("/api/claims/<int:claim_id>", methods=["PUT"])
def update_claim(claim_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in ["Pending", "Approved", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    conn = None
    cur = None

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

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

        conn.commit()
        return jsonify(claim)

    except psycopg2.Error:
        if conn:
            conn.rollback()
        app.logger.exception("Error while updating claim")
        return jsonify({"error": "Unable to update claim"}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    conn = None
    cur = None

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        password_hash = generate_password_hash(password)

        cur.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, name, email
        """, (name, email, password_hash))

        user = cur.fetchone()
        conn.commit()

        return jsonify(user), 201

    except psycopg2.errors.UniqueViolation:
        if conn:
            conn.rollback()
        return jsonify({"error": "Email already registered"}), 409

    except psycopg2.Error:
        if conn:
            conn.rollback()
        app.logger.exception("Database error during registration")
        return jsonify({"error": "Unable to register user"}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    conn = None
    cur = None

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

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
        app.logger.exception("Database error during login")
        return jsonify({"error": "Unable to log in"}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

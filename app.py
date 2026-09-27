import secrets
import string
from flask import Flask, jsonify, redirect, render_template, request
import database

# 1. Initialize Flask app
app = Flask(__name__)

# Available 62 characters: a-z, A-Z, 0-9
CHARACTERS = string.ascii_letters + string.digits


def generate_unique_code(length=6):
    """6-character ka unique code banata hai aur check karta hai DB mein duplicate na ho."""
    while True:
        code = "".join(secrets.choice(CHARACTERS) for _ in range(length))
        if not database.get_url_by_code(code):
            return code


# ---------------- ROUTES ---------------- #


# Route 1: Homepage (Frontend UI)
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        return """
        <h2>URL Shortener Backend is Live! 🚀</h2>
        <p>Frontend template banne tak aap API se test kar sakte hain.</p>
        """


# Route 2: Shorten API Endpoint (POST)
@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True) or request.form

    if not data or "url" not in data or not data["url"].strip():
        return jsonify({"error": "Valid 'url' field is required!"}), 400

    original_url = data["url"].strip()

    # Agar user ne http:// ya https:// nahi lagaya toh add karo
    if not (
        original_url.startswith("http://")
        or original_url.startswith("https://")
    ):
        original_url = "https://" + original_url

    # Unique code banakar database mein save karo
    short_code = generate_unique_code()
    database.save_url(original_url, short_code)

    # Full short link bana kar return karo
    short_url = f"{request.host_url}{short_code}"

    return (
        jsonify(
            {
                "success": True,
                "short_code": short_code,
                "short_url": short_url,
                "original_url": original_url,
            }
        ),
        201,
    )


# Route 3: The Redirect Route (GET /<short_code>)
@app.route("/<short_code>")
def redirect_to_url(short_code):
    """Jab koi short link khole, toh usko original website par redirect karo."""
    # Database se check karo
    row = database.get_url_by_code(short_code)

    if not row:
        return "<h3>404: Yeh short link exist nahi karta!</h3>", 404

    # Click count 1 se badhao
    database.increment_clicks(short_code)

    # HTTP 302 Redirect to destination
    return redirect(row["original_url"])


# Route 4: Analytics / Clicks check karne ke liye
@app.route("/api/stats/<short_code>")
def get_stats(short_code):
    row = database.get_url_by_code(short_code)
    if not row:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify(
        {
            "short_code": row["short_code"],
            "original_url": row["original_url"],
            "clicks": row["clicks"],
            "created_at": row["created_at"],
        }
    )


# ---------------- SERVER START ---------------- #
if __name__ == "__main__":
    database.init_db()  # DB table ensure karo
    app.run(port=5000, debug=True)
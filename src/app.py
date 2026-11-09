import os
import sys
from flask import Flask, jsonify, render_template, request

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
for p in (CURRENT_DIR, PARENT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    import seed_data
except ImportError:
    from src import seed_data

app = Flask(
    __name__,
    template_folder=os.path.join(CURRENT_DIR, "templates"),
    static_folder=os.path.join(CURRENT_DIR, "static"),
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "app": seed_data.APP_METADATA.get("title", "AnagramFrenzy"),
        "version": seed_data.APP_METADATA.get("version", "v1.3"),
    }), 200


@app.route("/api/catalog", methods=["GET"])
def catalog():
    category = request.args.get("category")
    persona_id = request.args.get("persona_id")
    search = request.args.get("search")
    return jsonify(seed_data.get_catalog(category=category, persona_id=persona_id, search=search)), 200


@app.route("/api/word/analyze", methods=["POST"])
def analyze_word_route():
    data = request.get_json(silent=True) or {}
    word = data.get("word", "")
    result = seed_data.start_or_analyze_word(word)
    status_code = 200 if result.get("valid") else 400
    return jsonify(result), status_code


@app.route("/api/word/guess", methods=["POST"])
def guess_word_route():
    data = request.get_json(silent=True) or {}
    word = data.get("word") or data.get("base_word") or ""
    guess = data.get("guess", "")
    return jsonify(seed_data.submit_isomeric_guess(word, guess)), 200


@app.route("/api/word/meaning", methods=["GET", "POST"])
def word_meaning_route():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        word = data.get("word", "")
    else:
        word = request.args.get("word", "")
    return jsonify(seed_data.get_word_meaning(word)), 200


@app.route("/api/word/shelve", methods=["POST"])
def shelve_word_route():
    data = request.get_json(silent=True) or {}
    word = data.get("word")
    return jsonify(seed_data.shelve_current_word(word)), 200


@app.route("/api/word/hint", methods=["POST"])
def hint_word_route():
    data = request.get_json(silent=True) or {}
    word = data.get("word")
    return jsonify(seed_data.reveal_remaining_words(word)), 200


@app.route("/api/interact", methods=["POST"])
def interact():
    data = request.get_json(silent=True) or {}
    result = seed_data.evaluate_interaction(data)
    return jsonify(result), 200


@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(seed_data.get_session_stats()), 200


@app.route("/api/daily", methods=["GET"])
def daily_challenge_route():
    date_param = request.args.get("date")
    return jsonify(seed_data.get_daily_challenge(date_param)), 200


@app.route("/api/reset", methods=["POST"])
def reset():
    return jsonify(seed_data.reset_session()), 200


@app.route("/api/export", methods=["GET"])
def api_export():
    data = seed_data.get_catalog()
    data["interoperability_format"] = "agentic_sd_catalog_v1"
    return jsonify(data), 200


@app.route("/api/schema", methods=["GET"])
def api_schema():
    items = getattr(seed_data, "CATALOG_ITEMS", [])
    sample_keys = sorted(list(items[0].keys())) if items and isinstance(items[0], dict) else []
    return jsonify({
        "contract_version": "1.3",
        "item_schema_keys": sample_keys,
        "endpoints": [
            "/health",
            "/api/catalog",
            "/api/word/analyze",
            "/api/word/guess",
            "/api/word/meaning",
            "/api/word/shelve",
            "/api/word/hint",
            "/api/interact",
            "/api/stats",
            "/api/reset",
            "/api/export",
            "/api/schema",
        ],
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
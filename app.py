import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename

from extractor import extract_text_from_pdf
from preprocessor import preprocess_text
from matcher import match_keywords
from scorer import compute_similarity
from suggestions import generate_suggestions
from database import init_db, save_analysis, get_all_analyses, get_analysis_by_id, delete_analysis

# ── App Configuration ─────────────────────────────────
app = Flask(__name__)
app.secret_key = "resume_analyzer_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Initialize Database ───────────────────────────────
init_db()

# ── Page Routes ───────────────────────────────────────

# Home
@app.route("/")
def landing():
    return render_template("landing.html")

# Module 1 — Upload & Analyze
@app.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")

# Module 2 — PDF Extraction
@app.route("/extractor")
def extractor_page():
    latest_id = session.get("latest_id")
    analysis = get_analysis_by_id(latest_id) if latest_id else None
    extracted = analysis["job_description"] if analysis else None
    return render_template("extractor.html", extracted=extracted)

# Module 3 — NLP Preprocessing
@app.route("/preprocessor")
def preprocessor_page():
    latest_id = session.get("latest_id")
    analysis = get_analysis_by_id(latest_id) if latest_id else None
    raw = analysis["job_description"] if analysis else None
    processed = " ".join(
        analysis["matched_keywords"] + analysis["missing_keywords"]
    ) if analysis else None
    return render_template("preprocessor.html", raw=raw, processed=processed)

# Module 4 — Keyword Matching
@app.route("/matcher")
def matcher_page():
    latest_id = session.get("latest_id")
    analysis = get_analysis_by_id(latest_id) if latest_id else None
    matched    = analysis["matched_keywords"]    if analysis else []
    missing    = analysis["missing_keywords"]    if analysis else []
    match_ratio = analysis["keyword_match_ratio"] if analysis else 0
    return render_template("matcher.html",
        matched=matched,
        missing=missing,
        match_ratio=match_ratio
    )

# Module 5 — Similarity Scoring
@app.route("/scorer")
def scorer_page():
    latest_id = session.get("latest_id")
    analysis = get_analysis_by_id(latest_id) if latest_id else None
    similarity_score    = analysis["similarity_score"]    if analysis else 0
    keyword_match_ratio = analysis["keyword_match_ratio"] if analysis else 0
    final_score         = analysis["final_score"]         if analysis else 0
    return render_template("scorer.html",
        similarity_score=similarity_score,
        keyword_match_ratio=keyword_match_ratio,
        final_score=final_score
    )

# Module 6 — Result Visualization
@app.route("/result")
def result_page():
    latest_id = session.get("latest_id")
    result = get_analysis_by_id(latest_id) if latest_id else None
    return render_template("result.html", result=result)

# Module 7 — Dashboard
@app.route("/dashboard")
def dashboard():
    analyses = get_all_analyses()
    return render_template("dashboard.html", analyses=analyses)

# View single analysis from dashboard
@app.route("/dashboard/<int:id>")
def view_analysis(id):
    analysis = get_analysis_by_id(id)
    return render_template("result.html", result=analysis)

# Delete analysis
@app.route("/dashboard/delete/<int:id>")
def delete_analysis_route(id):
    delete_analysis(id)
    return redirect(url_for("dashboard"))

# ── Main Analyze API ──────────────────────────────────
@app.route("/analyze", methods=["POST"])
def analyze():
    # Validate inputs
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded."}), 400

    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported."}), 400
    if not job_description:
        return jsonify({"error": "Job description cannot be empty."}), 400

    # Module 2 — Extract text
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        resume_raw = extract_text_from_pdf(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    if not resume_raw:
        return jsonify({"error": "Could not extract text from PDF."}), 400

    # Module 3 — Preprocess text
    resume_processed = preprocess_text(resume_raw)
    jd_processed     = preprocess_text(job_description)

    # Module 4 — Keyword matching
    keyword_results = match_keywords(resume_raw, job_description)

    # Module 5 — Similarity scoring
    similarity_score = compute_similarity(resume_processed, jd_processed)

    # Weighted final score
    final_score = round(
        (similarity_score * 0.6) + (keyword_results["match_ratio"] * 0.4), 2
    )

    # Module 6 — Generate suggestions
    suggestions = generate_suggestions(keyword_results["missing"], final_score)

    # Build result
    result = {
        "filename":             filename,
        "job_description":      job_description,
        "final_score":          final_score,
        "similarity_score":     similarity_score,
        "keyword_match_ratio":  keyword_results["match_ratio"],
        "matched_keywords":     keyword_results["matched"],
        "missing_keywords":     keyword_results["missing"],
        "total_jd_keywords":    keyword_results["total_jd_keywords"],
        "total_matched":        keyword_results["total_matched"],
        "suggestions":          suggestions,
    }

    # Save to DB and store only ID in session
    record_id = save_analysis(result)
    session["latest_id"] = record_id

    return jsonify(result)

# ── Run ───────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True, port=5000)
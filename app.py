import os
from flask import Flask, render_template, request, jsonify

from generator.qp_generator import generate_question_paper, extract_text_from_pdf, get_pdf_hash
import tempfile
from werkzeug.utils import secure_filename
app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("pdf")
    if not file:
        return "No file uploaded", 400

    # Make filename safe
    filename = secure_filename(file.filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        pdf_path = tmp.name

    # Generate SHA256 hash
    pdf_hash = get_pdf_hash(pdf_path)

    final_filename = f"{pdf_hash}.pdf"
    final_path = os.path.join(app.config["UPLOAD_FOLDER"], final_filename)

    if not os.path.exists(final_path):
        os.rename(pdf_path, final_path)
    else:
        os.remove(pdf_path)  

    text = extract_text_from_pdf(final_path)

    subject = (request.form.get("subject") or "General").strip()
    counts = {
        "mcq": int(request.form.get("mcq", 10)),
        "fib": int(request.form.get("fib", 10)),
        "short": int(request.form.get("short", 5)),
        "long": int(request.form.get("long", 4)),
    }

    paper = generate_question_paper(text, subject, counts)

    return render_template(
        "paper.html",
        paper=paper,
        subject=subject,
        counts=counts,
        pdf_hash=pdf_hash,
        pdf_file=final_filename
    )
@app.route("/generate", methods=["POST"])
def generate():
    text = (request.form.get("source_text") or "").strip()
    subject = (request.form.get("subject") or "General").strip() or "General"
    counts = {
        "mcq": int(request.form.get("mcq", 10)),
        "fib": int(request.form.get("fib", 10)),
        "short": int(request.form.get("short", 5)),
        "long": int(request.form.get("long", 4)),
    }
    paper = generate_question_paper(text, subject, counts)
    return render_template("paper.html", paper=paper, subject=subject, counts=counts)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    subject = (data.get("subject") or "General").strip() or "General"
    counts = {
        "mcq": int(data.get("mcq", 10)),
        "fib": int(data.get("fib", 10)),
        "short": int(data.get("short", 5)),
        "long": int(data.get("long", 4)),
    }
    paper = generate_question_paper(text, subject, counts)
    return jsonify(paper)

if __name__ == "__main__":
   
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

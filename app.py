import os
from flask import Flask, request, render_template
import json
from resumeparser import ats_extractor, _read_file_from_path

UPLOAD_PATH = r"__DATA__"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def ats():
    """
    Handles file upload and processing, extracts information from the uploaded resume.

    Returns:
        Rendered HTML page with extracted data.
    """
    # Ensure the upload path exists
    os.makedirs(UPLOAD_PATH, exist_ok=True)

    doc = request.files["pdf_doc"]
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    extracted_data = ats_extractor(doc_path)

    # return render_template("index.html", data=extracted_data)
    ## save the extracted data to a json file and show it prettily in the editor
    with open("extracted_data.json", "w") as f:
        json.dump(extracted_data, f)
    return render_template("index.html", data=extracted_data)


if __name__ == "__main__":
    app.run(port=8000, debug=True)

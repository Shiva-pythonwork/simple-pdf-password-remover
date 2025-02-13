from flask import Flask, render_template, request, send_file # type: ignore
import PyPDF2 # type: ignore
import os

app = Flask(__name__)

# Store unlocked PDF path
OUTPUT_PDF = "static/unlocked.pdf"

@app.route("/")
def index():
    return render_template("index.html", error=None, success=None, file_path=None)  

@app.route("/remove_password", methods=["POST"])
def remove_password():
    if "pdf_file" not in request.files:
        return render_template("index.html", error="No file selected", success=None, file_path=None)

    pdf_file = request.files["pdf_file"]
    password = request.form["password"]

    if pdf_file.filename == "":
        return render_template("index.html", error="Please upload a PDF file", success=None, file_path=None)

    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        if pdf_reader.is_encrypted:
            if not pdf_reader.decrypt(password):  # If password is incorrect
                return render_template("index.html", error="Incorrect password! Try again.", success=None, file_path=None)
        
        # Create new PDF without password
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Save the unlocked PDF
        with open(OUTPUT_PDF, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        return render_template("index.html", error=None, success="PDF unlocked successfully!", file_path=OUTPUT_PDF)

    except Exception as e:
        return render_template("index.html", error=f"Error: {str(e)}", success=None, file_path=None)

if __name__ == "__main__":
    app.run(debug=True)

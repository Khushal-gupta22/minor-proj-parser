import os
import google.generativeai as genai
import yaml
from pypdf import PdfReader


# Load API key from the configuration file
CONFIG_PATH = r"config.yaml"
UPLOAD_PATH = r"__DATA__"

api_key = None
with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data["GEMINI_API_KEY"]

# Set the Gemini API key
genai.configure(api_key=api_key)


def ats_extractor(resume_path):
    """
    Extracts information from the resume using the Google Gemini API.

    Args:
        resume_path (str): The path to the uploaded resume PDF.

    Returns:
        str: Parsed resume data as JSON string.
    """
    # Upload the resume to Gemini's File API
    uploaded_file = genai.upload_file(resume_path)

    # Choose a Gemini model and create a prompt
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = """ 
                You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
                1. Full Name
                2. Email ID
                3. GitHub Portfolio
                4. LinkedIn ID
                5. Employment Details
                6. Technical Skills
                7. Soft Skills
                8. Education Details
                9. Certifications
                10. Projects
                11. Awards
                and all the other essential details which are presnt in the resume.Give the extracted information in json format only.
        """

    # Process the uploaded file and get the response
    response = model.generate_content([prompt, uploaded_file])
    print(response.text)

    # Return the JSON result
    return response.text


def _read_file_from_path(path):
    """
    Reads the content of a PDF file and extracts text from it.

    Args:
        path (str): The file path to the PDF.

    Returns:
        str: Extracted text from the PDF.
    """
    reader = PdfReader(path)
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no]
        data += page.extract_text()

    return data

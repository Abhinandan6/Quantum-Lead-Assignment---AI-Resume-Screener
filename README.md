🚀 AI-Powered Resume Screening Agent
A semantic analysis tool designed to automate the manual screening of resumes. This prototype demonstrates how Large Language Models (LLMs) can parse unstructured candidate data (PDFs) and output structured decision logic (JSON) for downstream automation workflows.

The Problem
Recruitment teams face "Volume Fatigue."

Manual Bottleneck: Recruiters spend ~6 seconds per resume, leading to errors.

Keyword Bias: Traditional Applicant Tracking Systems (ATS) use rigid keyword matching (Regex), rejecting qualified candidates who use different terminology (e.g., rejecting "ReactJS" when looking for "React").

Unstructured Data: Resumes come in PDF/Docx formats, making data extraction difficult for automation tools.

The Solution
This agent replaces keyword matching with Semantic Reasoning.

Ingests unstructured PDF text.

Understands the context of a Job Description (JD).

Evaluates the candidate's fit based on skills, experience, and nuance.

Outputs a structured JSON payload containing a match_score, decision, and missing_skills.

Architecture & Workflow
This prototype serves as the "Intelligence Node" in a larger automation workflow.

Code snippet

Frontend: Streamlit (for prototype visualization).

Processing: Python + PyPDF2.

Intelligence: Qwen 2.5 Coder (via OpenRouter API).


⚙️ Installation & Setup
1. Clone the Repository
Bash

git clone https://github.com/Abhinandan6/Quantum-Lead-Assignment---AI-Resume-Screener.git
cd ai-resume-screener
2. Install Dependencies
Bash

pip install -r requirements.txt
3. Configure API Key
Get a free API Key from OpenRouter.

Open app.py and find the line:

Python

OPENROUTER_API_KEY = "PASTE_YOUR_OPENROUTER_KEY_HERE"
Paste your key inside the quotes.

4. Run the Application
Bash

streamlit run app.py
Prototype Screenshots
1. Analysis Dashboard
The agent extracts text, compares it against the specific JD requirements, and visualizes the fit. (Add a screenshot of your app here running successfully)



JSON - can be used if need to feed to n8n kind of tools

{
  "match_score": 85,
  "decision": "Interview",
  "missing_critical_skills": ["Docker"],
  "reasoning": "Candidate has strong Python experience but lacks containerization skills."
}
Tech Stack
Language: Python

Framework: Streamlit

LLM Provider: OpenRouter (Model: qwen/qwen-2.5-coder-32b-instruct)

PDF Parsing: PyPDF2

Future Improvements
n8n Integration: Deploy this script as a custom Python node within an n8n workflow.

Multi-File Upload: Allow batch processing of 50+ resumes at once.

Email Integration: Automatically fetch attachments from Gmail/Outlook.

Author: Abhinandan C AI Product Intern Assignment

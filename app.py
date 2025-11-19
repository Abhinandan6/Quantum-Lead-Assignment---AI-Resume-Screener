import streamlit as st
import requests
import PyPDF2
import json
import time

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# Custom CSS to make it look cleaner
st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
""", unsafe_allow_html=True)

# PASTE YOUR OPENROUTER KEY HERE
OPENROUTER_API_KEY = "Add API key here"

#2. HELPER FUNCTIONS 

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return ""

def analyze_candidate_openrouter(resume_text, jd_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", 
        "X-Title": "Resume Screener Student Project"
    }
    
    # IMPROVED PROMPT: Chain-of-Thought to reduce errors
    system_prompt = """
    You are a strict Technical Recruiter. 
    1. Read the Job Description (JD) carefully.
    2. Read the Candidate's Resume.
    3. Identify if they have the *Must-Have* skills mentioned in the JD.
    4. Output strictly VALID JSON.
    
    JSON Structure: 
    {
        "match_score": (integer 0-100), 
        "decision": ("Interview", "Hold", "Reject"), 
        "missing_critical_skills": ["skill1", "skill2"], 
        "reasoning": "Brief explanation of the score."
    }
    """
    # Choose any AI model from OpenRouter
    payload = {
        "model": "qwen/qwen-2.5-coder-32b-instruct:free", 
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"JD: {jd_text}\n\nRESUME: {resume_text}"}
        ],
        "response_format": {"type": "json_object"} 
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return {"error": f"API Error: {response.text}"}
        
        clean_json = response.json()['choices'][0]['message']['content'].replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        return {"error": f"Connection Error: {e}"}

# 3. SIDEBAR (CONTEXT) Frontend enhancement
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("AI Recruiter Pro")
    st.markdown("---")
    st.info("ℹ**How it works:**\n1. Upload a Resume (PDF).\n2. Define the Job.\n3. AI Agents analyze the fit.")
    st.markdown("---")
    st.caption("Built for n8n Automation Workflow Assignment")

# 4. MAIN INTERFACE - Took help of AI
st.title("Intelligent Resume Screening Agent")
st.markdown("#### Automating Talent Acquisition with LLMs")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Job Description")
    default_jd = """
    Role: Junior Python Developer
    Requirements:
    - Previous internship experience with Python and SQL.
    - Familiarity with Streamlit or Flask.
    - Good communication skills.
    """
    jd_input = st.text_area("Define the Role", height=300, value=default_jd, help="Paste the JD here.")

with col2:
    st.subheader("📄 Candidate Resume") #cv logo for ui
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", help="Drag and drop the resume here.")
    
    analyze_btn = st.button("Analyze Candidate Fit")

# 5. ANALYSIS LOGIC 
if analyze_btn:
    if "PASTE_YOUR" in OPENROUTER_API_KEY:
        st.error("API Key Missing in Code!")
    elif not uploaded_file:
        st.warning("Please upload a resume first.")
    else:
        # Progress Bar Animation (Visual Polish)
        progress_text = "Operation in progress. Please wait..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text="AI is reading the document...")
        
        text = extract_text_from_pdf(uploaded_file)
        if len(text) < 10:
            st.error("Could not extract text. Please try a text-based PDF.")
        else:
            result = analyze_candidate_openrouter(text, jd_input)
            my_bar.empty() # Remove progress bar
            
            if "error" in result:
                st.error(result['error'])
            else:
                # --- RESULT DASHBOARD --- #Generated using AI for better UI
                st.divider()
                
                # Top Metric Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Match Score", f"{result.get('match_score')}%")
                m2.metric("Decision", result.get('decision'))
                m3.metric("Status", "Processed")
                
                # Color-coded Feedback
                if result.get('decision') == "Interview":
                    st.success(f"**Analysis:** {result.get('reasoning')}")
                else:
                    st.warning(f"**Analysis:** {result.get('reasoning')}")
                
                # Missing Skills
                if result.get('missing_critical_skills'):
                    st.error(f"**Missing Critical Skills:** {', '.join(result.get('missing_critical_skills'))}")
                else:
                    st.success("No critical skills missing!")
                
                # JSON Output for n8n
                #with st.expander("🔌 View JSON Payload (For n8n Automation)"):
                    #st.code(json.dumps(result, indent=2), language='json')
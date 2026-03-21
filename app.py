import streamlit as st
import PyPDF2
from groq import Groq

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume_with_ai(resume_text, job_description):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = f"""
You are an expert resume analyzer and career coach.

Analyze the resume below against the job description and provide:
1. Match Score (0-100%)
2. Top 5 Matching Skills found in resume
3. Top 5 Missing Skills not in resume but required in job
4. 3 Specific suggestions to improve the resume

Resume:
{resume_text}

Job Description:
{job_description}

Reply in this exact format:
MATCH SCORE: [number]%

MATCHING SKILLS:
- skill 1
- skill 2
- skill 3
- skill 4
- skill 5

MISSING SKILLS:
- skill 1
- skill 2
- skill 3
- skill 4
- skill 5

SUGGESTIONS:
- suggestion 1
- suggestion 2
- suggestion 3
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content

# --- UI ---
st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")
st.title("📄 Resume Analyzer AI")
st.subheader("See how well your resume matches a job description")

st.markdown("### Step 1: Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

st.markdown("### Step 2: Paste the Job Description")
job_description = st.text_area("Paste the job description here", height=200)

if st.button("🔍 Analyze My Resume"):
    if not uploaded_file:
        st.warning("Please upload your resume first!")
    elif not job_description:
        st.warning("Please paste a job description!")
    else:
        with st.spinner("AI is analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume_with_ai(resume_text, job_description)

        st.success("Analysis Complete!")
        st.markdown("---")
        st.markdown("## AI Analysis Result")
        st.markdown(result)

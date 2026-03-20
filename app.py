import streamlit as st
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- UI ---
st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")
st.title("📄 Resume Analyzer AI")
st.subheader("See how well your resume matches a job description")

# Upload resume
st.markdown("### Step 1: Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

# Paste job description
st.markdown("### Step 2: Paste the Job Description")
job_description = st.text_area("Paste the job description here", height=200)

# Analyze button
if st.button("🔍 Analyze My Resume"):
    if not uploaded_file:
        st.warning("Please upload your resume first!")
    elif not job_description:
        st.warning("Please paste a job description!")
    else:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Resume uploaded successfully!")
        st.markdown("### Extracted Resume Text (Preview)")
        st.write(resume_text[:500] + "...")
        st.info("🤖 AI Analysis coming next!")

import streamlit as st
import fitz
import re
import google.generativeai as genai

st.set_page_config(page_title="Fact Check Agent", layout="wide")

st.title("📄 Fact-Check Agent")
st.write("Upload a PDF and verify claims against AI/web knowledge.")

API_KEY = st.text_input("Enter Gemini API Key", type="password")

def extract_text(pdf_file):
    text = ""
    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_claims(text):
    pattern = r'\b\d+[%]?[^.]*\.'
    claims = re.findall(pattern, text)
    return claims[:10]

def verify_claims(claims):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    results = []

    for claim in claims:
        prompt = f"""
        Verify this claim using latest public knowledge:
        Claim: {claim}

        Return:
        Status: Verified / Inaccurate / False
        Correct Fact:
        Reason:
        """
        response = model.generate_content(prompt)
        results.append((claim, response.text))

    return results

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded and API_KEY:
    text = extract_text(uploaded)
    claims = extract_claims(text)

    st.subheader("Extracted Claims")
    for c in claims:
        st.write("•", c)

    if st.button("Verify Claims"):
        output = verify_claims(claims)

        st.subheader("Results")
        for claim, result in output:
            st.markdown(f"### Claim\n{claim}")
            st.markdown(result)
            st.divider()

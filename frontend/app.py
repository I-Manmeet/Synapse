import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Synapse Business Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Synapse Business Assistant")
st.write("AI-powered Multi-Agent Business Analysis")

st.divider()

# -------------------------
# FILE UPLOAD
# -------------------------

st.subheader("📁 Upload Business Document")

uploaded_file = st.file_uploader(
    "Upload PDF, DOCX, Excel, CSV or TXT",
    type=["pdf", "docx", "xlsx", "xls", "csv", "txt"]
)

if uploaded_file is not None:

    if st.button("Upload Document"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        try:

            response = requests.post(
                f"{BACKEND_URL}/upload",
                files=files
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    f"✅ {data['filename']} uploaded successfully!"
                )

            else:

                st.error(
                    f"Upload failed: {response.text}"
                )

        except Exception as e:

            st.error(f"Backend connection error: {e}")


st.divider()

# -------------------------
# BUSINESS QUESTION
# -------------------------

st.subheader("💬 Ask Your Business Question")

question = st.text_area(
    "What would you like to know?",
    placeholder=(
        "Example: Analyze my business performance "
        "and explain the main reasons for the sales decline."
    ),
    height=120
)

if st.button("🚀 Analyze Business"):

    if not question.strip():

        st.warning("Please enter a business question.")

    else:

        with st.spinner(
            "🤖 Synapse agents are analyzing your business..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={
                        "question": question,
                        "context": ""
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("✅ Analysis completed!")

                    st.divider()

                    st.subheader("📋 Business Report")

                    st.markdown(data["report"])

                else:

                    st.error(
                        f"Analysis failed: {response.text}"
                    )

            except Exception as e:

                st.error(
                    f"Backend connection error: {e}"
                )
import streamlit as st
from google import genai
from dotenv import load_dotenv
from pypdf import PdfReader
import os


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Main Container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

/* Main Title */
.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(to right, #8B5CF6, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

/* Subtitle */
.subtitle {
    color: #9CA3AF;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}


/* Chat Response */
.response-box {
    background-color: #161B22;
    padding: 1.5rem;
    border-radius: 18px;
    border: 1px solid #2D3748;
    margin-top: 1rem;
}

/* Sidebar */
.css-1d391kg {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)


# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


# =========================================
# GEMINI CLIENT
# =========================================

client = genai.Client(api_key=api_key)


# =========================================
# SESSION STATE
# =========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.title("📘 AI Research Assistant")

    st.markdown("---")

    st.markdown("""
    ### Features
    
    ✅ Upload PDFs  
    ✅ Ask questions  
    ✅ AI summaries  
    ✅ Research assistance  
    ✅ Instant analysis  
    """)

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    st.info("Powered by Gemini 2.5 Flash")


# =========================================
# HEADER
# =========================================

st.markdown(
    '<div class="main-title">AI Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload PDFs and interact with documents using AI-powered research assistance.</div>',
    unsafe_allow_html=True
)


# =========================================
# LAYOUT COLUMNS
# =========================================

left_col, right_col = st.columns([1, 2])


# =========================================
# LEFT COLUMN
# =========================================

# =========================================
# LEFT COLUMN
# =========================================

with left_col:

    st.subheader("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "",
        type="pdf"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("💬 Ask Questions")

    user_question = st.text_area(
        "",
        height=180,
        placeholder="Ask anything about the document..."
    )

    ask_button = st.button(
        "🚀 Analyze Document",
        use_container_width=True
    )

# =========================================
# RIGHT COLUMN
# =========================================

with right_col:

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    st.subheader("🤖 AI Responses")

    if uploaded_file is not None:

        pdf_reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text

        st.success("✅ PDF processed successfully")



        # =========================================
        # PDF SUMMARY
        # =========================================

        with st.expander("📑 Generate PDF Summary"):

            if st.button("Generate Summary"):

                summary_prompt = f"""
                Summarize the following PDF in simple and clear points:

                {pdf_text}
                """

                with st.spinner("Generating summary..."):

                    summary_response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=summary_prompt
                    )

                st.write(summary_response.text)



        # =========================================
        # QUESTION ANSWERING
        # =========================================

        if ask_button and user_question:

            prompt = f"""
            Answer the question based on the PDF below.

            PDF Content:
            {pdf_text}

            Question:
            {user_question}
            """

            with st.spinner("🤖 AI is analyzing your document..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            # Store chat history
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": response.text
            })


    # =========================================
    # CHAT HISTORY
    # =========================================

    for chat in reversed(st.session_state.chat_history):

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

    st.markdown('</div>', unsafe_allow_html=True)
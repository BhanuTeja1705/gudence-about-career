import streamlit as st
import google.generativeai as genai

# ----- Gemini API Setup -----
genai.configure(api_key="AIzaSyAOz1lt8GWmd8T5J8p5Ldr-_yzkb-vyAVI")  # Replace with your actual key
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❗ Error: {str(e)}"


# ----- Page Configuration -----
st.set_page_config(
    page_title="AI Career Coach",
    layout="wide",
    page_icon="🚀"
)

# ----- Custom CSS Styling -----
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #121212; color: #f5f5f5; font-family: 'Segoe UI', sans-serif; }
    .css-1d391kg { background-color: #1F1F1F !important; }
    .main-header { font-size: 3rem; color: #ffffff; text-align: center; font-weight: bold; padding-bottom: 10px; }
    .subtitle { font-size: 1.3rem; color: #bbbbbb; text-align: center; margin-bottom: 30px; }
    .stTabs [role="tablist"] { background-color: #1E1E1E; border-radius: 12px; padding: 0.5rem; }
    .stTabs [data-baseweb="tab-panel"] { background-color: #1E1E1E; padding: 1.5rem; border-radius: 10px; box-shadow: 0px 8px 20px rgba(0,0,0,0.4); }
    input, textarea { background-color: #2C2F33 !important; color: #f5f5f5 !important; border: 1px solid #444444 !important; border-radius: 8px !important; padding: 10px; }
    .stButton button { background-color: #4CAF50 !important; color: white !important; border-radius: 8px; padding: 10px 20px; border: none; transition: all 0.3s ease; }
    .stButton button:hover { background-color: #45a049 !important; transform: translateY(-2px); box-shadow: 0px 4px 12px rgba(76, 175, 80, 0.3); }
    .card { background-color: #2C2F33; padding: 1.5rem; border-radius: 15px; box-shadow: 0px 8px 20px rgba(0,0,0,0.3); margin-bottom: 2rem; }
    .icon { font-size: 2rem; color: #03A9F4; margin-right: 10px; }
    .footer { text-align: center; padding: 1rem; color: #888888; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# ----- Sidebar -----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("## AI Career Coach")
    st.markdown("Welcome to your AI-powered career consultant! 🚀")
    st.markdown("### Features")
    st.markdown("✅ Career Advice")
    st.markdown("✅ Resume Review")
    st.markdown("✅ Skill Learning Path")
    st.markdown("✅ Mock Interviews")
    st.markdown("✅ Market Insights")

# ----- Main Title -----
st.markdown('<div class="main-header">🚀 Welcome to AI Career Coach</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI-powered career advisor and mentor!</div>', unsafe_allow_html=True)

# ----- Tabs -----
tabs = st.tabs(["Career Guidance", "Resume Review", "Learning Path", "Mock Interview", "Market Insights"])

# ----- Tab 1: Career Guidance -----
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Personalized Career Advice")

    user_name = st.text_input("Enter your name", placeholder="John Doe")
    user_background = st.text_area("Tell us about your background and interests",
                                   placeholder="E.g., I have a background in computer science and I'm interested in AI and machine learning.")

    if st.button("Get Career Suggestions"):
        if user_name and user_background:
            prompt = f"""
            Act as a professional career coach.
            User's Name: {user_name}
            Background and Interests: {user_background}

            Provide 4 tailored career suggestions with reasons, and give actionable advice for the next steps.
            """
            response = get_gemini_response(prompt)
            st.success(f"Hi {user_name}! Here's your personalized career guidance:")
            st.markdown(response)
        else:
            st.warning("Please fill in your name and background to get suggestions.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 2: Resume Review -----
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📝 Resume Review")
    st.markdown("Upload your resume (PDF format) to get AI feedback:")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

    if st.button("Analyze Resume"):
        if uploaded_file:
            st.success("✅ Analyzing your resume...")
            resume_text = "Sample extracted text from resume (simulated)"  # Replace with actual PDF text extraction
            prompt = f"""
            You are a professional resume reviewer.
            Review the following resume content and provide suggestions to improve it. Focus on clarity, achievements, and ATS optimization.

            Resume Content:
            {resume_text}
            """
            response = get_gemini_response(prompt)
            st.markdown(response)
        else:
            st.warning("Please upload your resume for analysis.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 3: Learning Path -----
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📚 Personalized Learning Path")

    selected_field = st.selectbox("Select your career goal",
                                  ["Data Science", "Web Development", "AI/ML", "Cybersecurity", "Product Management"])

    if st.button("Generate Learning Path"):
        prompt = f"""
        Provide a detailed and personalized 6-month learning roadmap for a beginner in {selected_field}.
        Include courses, projects, certifications, and practical tips to succeed in this field.
        """
        response = get_gemini_response(prompt)
        st.success(f"🚀 Learning Path for {selected_field}")
        st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 4: Mock Interview -----
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎤 Mock Interview Practice")

    field = st.selectbox("Select your domain", ["Software Engineering", "Data Science", "Product Management"])

    if st.button("Start Mock Interview"):
        prompt = f"""
        Act as an interviewer for a {field} role.
        Ask one challenging interview question and provide a brief guideline on how to answer it effectively.
        """
        response = get_gemini_response(prompt)
        st.info(f"Here is a sample question for {field}:")
        st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 5: Market Insights -----
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Market Insights")

    if st.button("Show Market Trends"):
        prompt = """
        Provide the latest insights on job market trends for 2025.
        Focus on in-demand tech skills, job roles, salary trends, and remote opportunities.
        """
        response = get_gemini_response(prompt)
        st.success("✅ Latest Market Trends")
        st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Footer -----
st.markdown('<div class="footer">© 2025 AI Career Coach. All rights reserved.</div>', unsafe_allow_html=True)

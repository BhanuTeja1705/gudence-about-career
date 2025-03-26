import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF text extraction
import os

# ----- Gemini API Setup -----
genai.configure(api_key="AIzaSyDPAjI3VeKDVaQ_5LB61owH1uZJoiQjKiU")

# Initialize the Gemini Model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# ----- Functions -----
def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❗ Error: {str(e)}"

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"❗ Error extracting text: {str(e)}"

def translate_prompt(base_prompt, language):
    translations = {
        "English": base_prompt,
        "Hindi": f"नीचे दी गई जानकारी के आधार पर सुझाव दें:\n{base_prompt}",
        "Telugu": f"కింద ఇవ్వబడిన సమాచారం ఆధారంగా సూచనలు ఇవ్వండి:\n{base_prompt}",
        "Tamil": f"கீழே வழங்கப்பட்ட தகவலின் அடிப்படையில் பரிந்துரைகளை வழங்கவும்:\n{base_prompt}"
    }
    return translations.get(language, base_prompt)

# ----- Streamlit Page Configuration -----
st.set_page_config(
    page_title="AI Career Coach",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# ----- Custom CSS Styling (Background Image and Transparency) -----
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
        }
        [data-testid="stAppViewContainer"] {
            background-image: url('https://i.pinimg.com/736x/8a/b8/1e/8ab81e729a8de18414f4bf38ca10fe92.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .main-header {
            font-size: 40px;
            color: #2E86C1;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 20px;
            color: #566573;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            color: #ffffff;
            background-color: rgba(0,0,0,0.5);
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# ----- Sidebar -----
with st.sidebar:
    st.image("https://i.pinimg.com/736x/cb/3c/ef/cb3cefbcba842dc7a34c0dfafcf38858.jpg", width=100)
    st.markdown("## AI Career Coach")
    st.markdown("Welcome to your AI-powered career consultant! 🚀")

    # Language Selection
    language = st.selectbox("🌐 Select Language", ["English", "Hindi", "Telugu", "Tamil"])

    st.markdown("### Features")
    st.markdown("""
        ✅ Career Advice  
        ✅ Resume Review  
        ✅ Skill Learning Path  
        ✅ Mock Interviews  
        ✅ Market Insights
    """)
    st.markdown("---")
    st.markdown("ℹ️ Ensure you upload PDF resumes under 5MB for the best experience.")

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
    user_background = st.text_area(
        "Tell us about your background and interests",
        placeholder="E.g., I have a background in computer science and I'm interested in AI and machine learning."
    )

    if st.button("Get Career Suggestions", key="career_suggestions"):
        if user_name and user_background:
            with st.spinner("Crafting your personalized career guidance..."):
                base_prompt = f"""
                Act as an experienced career coach. Based on the following user details, provide 4 tailored career suggestions with reasons.
                Also, include actionable next steps.

                User's Name: {user_name}  
                Background and Interests: {user_background}

                Format your response with bullet points and bold key takeaways.
                """
                localized_prompt = translate_prompt(base_prompt, language)
                response = get_gemini_response(localized_prompt)

                if "❗ Error" in response:
                    st.error(response)
                else:
                    st.success(f"Hi {user_name}! Here's your personalized career guidance:")
                    st.markdown(response)
        else:
            st.warning("Please fill in your name and background.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 2: Resume Review -----
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📝 Resume Review")
    st.markdown("Upload your resume (PDF format) to get AI feedback:")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

    if st.button("Analyze Resume", key="analyze_resume"):
        if uploaded_file:
            with st.spinner("Extracting and analyzing your resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)

                if resume_text.startswith("❗ Error"):
                    st.error(resume_text)
                else:
                    base_prompt = f"""
                    You are an expert resume reviewer. Analyze the following resume content and suggest improvements focused on:

                    1. **Clarity**: Clear language, concise descriptions.  
                    2. **Achievements**: Quantified impact, results-oriented statements.  
                    3. **ATS Optimization**: Relevant keywords, easy parsing by Applicant Tracking Systems.

                    Provide feedback in a structured format: Strengths ✅, Suggestions 🔧, and Example Improvements 📝.

                    Resume Content:  
                    {resume_text}
                    """
                    localized_prompt = translate_prompt(base_prompt, language)
                    response = get_gemini_response(localized_prompt)

                    if "❗ Error" in response:
                        st.error(response)
                    else:
                        st.success("✅ Resume Review Completed!")
                        st.markdown(response)
        else:
            st.warning("Please upload your resume.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 3: Learning Path -----
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📚 Personalized Learning Path")

    selected_field = st.selectbox("Select your career goal", [
        "Data Science", "Web Development", "AI/ML", "Cybersecurity", "Product Management"
    ])

    if st.button("Generate Learning Path", key="learning_path"):
        with st.spinner("Generating your learning roadmap..."):
            base_prompt = f"""
            Create a personalized 6-month learning roadmap for a beginner interested in {selected_field}.
            Include:  
            - Essential skills to learn  
            - Recommended courses (free/paid)  
            - Capstone project ideas  
            - Industry certifications  
            - Practical tips for career growth  
            Format it in bullet points.
            """
            localized_prompt = translate_prompt(base_prompt, language)
            response = get_gemini_response(localized_prompt)

            if "❗ Error" in response:
                st.error(response)
            else:
                st.success(f"🚀 Learning Path for {selected_field}")
                st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 4: Mock Interview -----
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎤 Mock Interview Practice")

    field = st.selectbox("Select your domain", [
        "Software Engineering", "Data Science", "Product Management", "Cybersecurity"
    ])

    if st.button("Start Mock Interview", key="mock_interview"):
        with st.spinner("Fetching a challenging interview question..."):
            base_prompt = f"""
            Act as an expert interviewer for a {field} role.
            Ask one challenging interview question and provide a sample high-quality answer with key points to cover.
            """
            localized_prompt = translate_prompt(base_prompt, language)
            response = get_gemini_response(localized_prompt)

            if "❗ Error" in response:
                st.error(response)
            else:
                st.info(f"Mock Interview Question for {field}:")
                st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Tab 5: Market Insights -----
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Market Insights")

    if st.button("Show Market Trends", key="market_trends"):
        with st.spinner("Gathering the latest job market insights..."):
            base_prompt = """
            Provide the latest job market insights for 2025 focusing on:
            - In-demand tech skills  
            - Top job roles  
            - Salary trends by region  
            - Remote work opportunities  
            Present it in bullet points.
            """
            localized_prompt = translate_prompt(base_prompt, language)
            response = get_gemini_response(localized_prompt)

            if "❗ Error" in response:
                st.error(response)
            else:
                st.success("✅ Latest Market Trends")
                st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Footer -----
st.markdown('<div class="footer">© 2025 AI Career Coach. All rights reserved.Created By Bhanuteja🤍</div>', unsafe_allow_html=True)

import os
import re

import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Critic",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# =========================================================
# SESSION STATE
# =========================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "improvement_plan" not in st.session_state:
    st.session_state.improvement_plan = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_pdf_text(pdf_file):
    """Extract text from an uploaded PDF file."""

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_score(text, label):
    """
    Extract the actual score from Gemini's response.

    Supports:
        65/100
        72%
    """

    # Look for X/100
    match = re.search(
        rf"{re.escape(label)}.*?(\d{{1,3}})\s*/\s*100",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return int(match.group(1))

    # Look for X%
    match = re.search(
        rf"{re.escape(label)}.*?(\d{{1,3}})\s*%",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return int(match.group(1))

    return None


def analyze_resume(resume, job_description):

    prompt = f"""
You are NOT a friendly career coach.

You are a ruthless Silicon Valley technical recruiter
who has reviewed thousands of resumes and has very little
patience for vague, generic, exaggerated, or poorly written
resume content.

Your job is to decide whether this candidate deserves
an interview for the SPECIFIC job below.

You must be brutally honest, sarcastic when appropriate,
and direct.

IMPORTANT:

Do NOT insult the candidate personally.

Roast the RESUME, not the person.

Do NOT invent skills, experience, projects, companies,
achievements, certifications, or technologies.

If the candidate does not have a required skill,
say that clearly.

=============================
CANDIDATE RESUME
=============================

{resume}

=============================
TARGET JOB DESCRIPTION
=============================

{job_description}

=============================
YOUR JOB
=============================

Analyze this resume like a ruthless Silicon Valley
technical recruiter.

Focus especially on:

1. Missing job-description keywords.

2. Skills required by the JD that are absent from
   the resume.

3. Weak, vague, generic, or unimpressive bullet points.

4. Lack of measurable achievements.

5. Poor use of technical terminology.

6. Experience mismatches.

7. Claims that are not supported by evidence.

8. Whether the candidate would realistically get
   shortlisted for THIS job.

=============================
OUTPUT FORMAT
=============================

Use EXACTLY these sections.

# 🎯 RECRUITER SCORE

Overall Resume Score: X/100

ATS Compatibility Score: X/100

Estimated Skill Match: X%

Give a one-sentence explanation for the score.

# 🎯 SHORTLIST VERDICT

Choose EXACTLY ONE , express in a bold way 

✅ SHORTLIST

⚠️ MAYBE

❌ REJECT

Then explain the decision in 2-4 sentences.

# 🔎 MISSING KEYWORDS

List the most important keywords from the JD that
are missing from the resume.

For every keyword, explain briefly why it matters.

Prioritize critical keywords instead of dumping
every word from the JD.

# ⚠️ WEAK BULLET POINTS

Identify up to 5 weak bullet points.

For EACH weak bullet:


## 💀 ROAST
Give a short ruthless recruiter-style critique.

Make it witty and direct.

Example style:

"Worked on" tells me absolutely nothing.
Did you build it, break it, deploy it,
or just watch someone else do it?

## ✅ BETTER VERSION
Rewrite the  bullet to be stronger.

IMPORTANT:
Do NOT invent metrics or achievements.

If the original bullet does not provide a metric,
use a placeholder such as [X%] rather than inventing one.



# 💎 STRONGEST PARTS

Identify the 3 strongest parts of the resume
that actually help the candidate for this JD.

Do not give fake praise.

# 🔥 SILICON VALLEY ROAST

Give a brutally honest paragraph about this resume.

This should sound like a recruiter who has 30 seconds
to decide whether to continue reading.

Use humor and sarcasm where appropriate.

Example tone:

"Your Java experience is solid. Unfortunately,
the job wants Python. That's not a minor typo;
that's walking into a Python interview wearing
a Java T-shirt and hoping nobody notices."

# 🚨 BIGGEST RED FLAGS

Identify the 3 biggest reasons this resume could
be rejected for this specific job.

Be direct.

Again:
Roast the resume, NOT the candidate.





Prioritize changes by impact.

=============================
IMPORTANT RULES
=============================

1. Be ruthless but useful.

2. Do not become abusive.

3. Do not make generic career statements.

4. Every criticism must connect to the resume
   or the target JD.

5. Never invent experience.

6. Never tell the candidate to add a skill they
   don't actually have.

7. Never invent statistics.

8. If a metric is missing, recommend adding a real
   metric rather than creating one.

9. Keep the roast entertaining but technically useful.

10. The goal is not to make the candidate feel good.

The goal is to make the resume significantly better
for THIS job. 
ask whether he needed any fixes , if yes 

# 🛠️ TOP 5 FIXES

Give the five highest-impact changes the candidate
should make before applying to this specific job.

Now perform the analysis.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text



def generate_improvement_plan(resume, job_description, analysis):

    prompt = f"""
You are a senior resume strategist helping a candidate
tailor their resume for a specific job.

Use the candidate's existing resume, target job description,
and previous recruiter analysis.

========================
RESUME
========================

{resume}

========================
JOB DESCRIPTION
========================

{job_description}

========================
PREVIOUS ANALYSIS
========================

{analysis}

========================
TASK
========================

Create a practical resume improvement plan.

Explain:


2. Which skills should be highlighted.

3. Which missing keywords should naturally be added.

4. Which experience bullets should be rewritten.

5. Which projects should be highlighted or removed.

6. What technical achievements should be quantified.



8. Give an example of an improved professional summary.

9. Give a final priority list:
    HIGH PRIORITY

    
Do not invent experience or skills that are not present
in the original resume.

ask whether the candiate wants to rewrite their resume summary, and if so, provide a rewritten version and explain why it is better for this job.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def recruiter_chat(question):

    prompt = f"""
You are the AI recruiter inside an AI Resume Critic application.

You already know the candidate's resume,
the target job description and the previous analysis.

========================
RESUME
========================

{st.session_state.resume_text}

========================
JOB DESCRIPTION
========================

{st.session_state.job_description}

========================
PREVIOUS ANALYSIS
========================

{st.session_state.analysis}

========================
CONVERSATION
========================

{st.session_state.chat_history}

========================
USER QUESTION
========================

{question}

Answer specifically using the candidate's actual resume
and the target job.

Do not invent experience.

If the user asks for a rewrite, provide the rewritten version
and briefly explain why it is better for this job.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# =========================================================
# HEADER
# =========================================================

st.title("📄 AI Resume Critic")

st.markdown(
    "### ATS & Job Match Analyzer"
)

st.write(
    "Upload your resume, compare it against a target job, "
    "and get recruiter-level feedback."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Resume Critic")

    st.markdown(
        """
        **What this AI does**

        📄 Reads your resume

        💼 Understands the target job

        🔍 Finds skill gaps

        🎯 Identifies missing keywords

        🤖 Gives recruiter feedback

        ✍️ Suggests improvements
        """
    )

    st.divider()

    if st.session_state.resume_text:

        st.success("Resume loaded")

    if st.session_state.job_description:

        st.success("Job description loaded")


# =========================================================
# INPUT SECTION (resume + job description)
# =========================================================
# NOTE: this is a plain container, not st.form(), because the
# Upload/Paste toggle needs to rerun the page immediately when
# switched — st.form only reruns on submit, which would make the
# toggle appear frozen.

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📄 Upload Resume")

    resume_mode = st.radio(
        "How would you like to provide your resume?",
        options=["Upload PDF", "Paste Text"],
        horizontal=True,
        key="resume_input_mode"
    )

    if resume_mode == "Upload PDF":

        resume_file = st.file_uploader(
            "Upload your PDF resume",
            type=["pdf"],
            help="Upload a text-based PDF resume.",
            key="resume_pdf_uploader"
        )

        if resume_file is not None:

            try:
                extracted_text = extract_pdf_text(resume_file)

                if extracted_text.strip():
                    st.session_state.resume_text = extracted_text
                    st.success(f"✅ Extracted text from **{resume_file.name}**")

                    with st.expander("Preview extracted text"):
                        st.text_area(
                            "Extracted resume text",
                            value=extracted_text,
                            height=200,
                            disabled=True
                        )
                else:
                    st.warning(
                        "⚠️ Couldn't extract any text from this PDF. "
                        "It might be a scanned image — try pasting the text instead."
                    )

            except Exception as e:
                st.error(f"❌ Failed to read PDF: {e}")

    else:  # Paste Text

        pasted_resume = st.text_area(
            "Paste your resume text here",
            value=st.session_state.resume_text,
            height=230,
            placeholder="Paste your resume content here...",
            key="resume_paste_area"
        )

        st.session_state.resume_text = pasted_resume

    if st.session_state.resume_text.strip():
        word_count = len(st.session_state.resume_text.split())
        st.caption(f"📝 Resume loaded — approx. {word_count} words")
    else:
        st.caption("No resume provided yet.")

with col2:

    st.markdown("### 💼 Target Job")

    job_description = st.text_area(
        "Paste the job description",
        height=280,
        placeholder="Paste the complete job description here...",
        key="job_description_area"
    )

st.divider()

analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True,
    type="primary"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if not API_KEY:

        st.error(
            "Gemini API key not found. "
            "Please check your .env file."
        )

    elif not st.session_state.resume_text.strip():

        st.warning(
            "Please provide your resume (upload a PDF or paste the text)."
        )

    elif not job_description.strip():

        st.warning(
            "Please enter the target job description."
        )

    else:

        st.session_state.job_description = job_description

        with st.spinner(
            "🤖 AI Recruiter is analyzing your resume..."
        ):

            try:

                analysis = analyze_resume(
                    st.session_state.resume_text,
                    st.session_state.job_description
                )

                st.session_state.analysis = analysis

                # Reset previous conversation
                st.session_state.chat_history = []

                # Reset previous improvement plan
                st.session_state.improvement_plan = None

            except Exception as e:

                st.error(
                    f"Gemini API error: {e}"
                )


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.analysis:

    st.divider()

    st.markdown("## 📊 Resume Performance Dashboard")

    analysis = st.session_state.analysis

    overall_score = extract_score(
        analysis,
        "Overall Resume Score"
    )

    ats_score = extract_score(
        analysis,
        "ATS Compatibility Score"
    )

    skill_match = extract_score(
        analysis,
        "Estimated Skill Match"
    )

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🎯 Overall Score",
            f"{overall_score}/100"
            if overall_score is not None
            else "N/A"
        )

    with col2:

        st.metric(
            "🤖 ATS Score",
            f"{ats_score}/100"
            if ats_score is not None
            else "N/A"
        )

    with col3:

        st.metric(
            "🧠 Skill Match",
            f"{skill_match}%"
            if skill_match is not None
            else "N/A"
        )

    with col4:

        st.metric(
            "📄 Resume",
            "Analyzed"
        )


    # -----------------------------------------------------
    # SCORE VISUALIZATION
    # -----------------------------------------------------

    st.markdown("### 📈 Score Overview")

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:

        st.markdown("**Overall Resume Score**")

        if overall_score is not None:
            st.progress(
                min(overall_score, 100)
            )

            st.caption(
                f"{overall_score}/100"
            )

    with score_col2:

        st.markdown("**ATS Compatibility**")

        if ats_score is not None:
            st.progress(
                min(ats_score, 100)
            )

            st.caption(
                f"{ats_score}/100"
            )

    with score_col3:

        st.markdown("**Skill Match**")

        if skill_match is not None:
            st.progress(
                min(skill_match, 100)
            )

            st.caption(
                f"{skill_match}%"
            )


    # =====================================================
    # ANALYSIS TABS
    # =====================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "🔍 Recruiter Analysis",
            "💡 Improve My Resume",
            "🤖 Ask Recruiter"
        ]
    )


    # =====================================================
    # TAB 1
    # =====================================================

    with tab1:

        st.markdown(
            "### 🤖 Recruiter Assessment"
        )

        st.markdown(
            analysis
        )


    # =====================================================
    # TAB 2
    # =====================================================

    with tab2:

        st.markdown(
            "### 💡 How Should I Improve My Resume?"
        )

        st.write(
            "Generate a personalized improvement plan "
            "based on your resume and this job description."
        )

        if st.button(
            "✨ Generate Improvement Plan",
            type="primary"
        ):

            with st.spinner(
                "🧠 Building your personalized resume strategy..."
            ):

                try:

                    improvement_plan = generate_improvement_plan(
                        st.session_state.resume_text,
                        st.session_state.job_description,
                        st.session_state.analysis
                    )

                    st.session_state.improvement_plan = (
                        improvement_plan
                    )

                except Exception as e:

                    st.error(
                        f"Gemini error: {e}"
                    )


        if st.session_state.improvement_plan:

            st.divider()

            st.markdown(
                st.session_state.improvement_plan
            )


    # =====================================================
    # TAB 3 — CONVERSATIONAL RECRUITER
    # =====================================================

    with tab3:

        st.markdown(
            "### 🤖 Ask Your AI Recruiter"
        )

        st.caption(
            "Ask questions about how to tailor your resume "
            "for this specific job."
        )


        # -----------------------------------------------
        # Previous conversation
        # -----------------------------------------------

        for message in st.session_state.chat_history:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )


        # -----------------------------------------------
        # Chat input
        # -----------------------------------------------

        question = st.chat_input(
            "Ask: How should I rewrite my summary?"
        )


        if question:

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):

                st.markdown(question)


            with st.chat_message("assistant"):

                with st.spinner(
                    "Recruiter is thinking..."
                ):

                    try:

                        answer = recruiter_chat(
                            question
                        )

                        st.markdown(answer)

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    except Exception as e:

                        st.error(
                            f"Gemini error: {e}"
                        )

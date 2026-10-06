import streamlit as st
from langchain_ollama import ChatOllama


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
   REMOVE TOP WHITE SPACE
========================================================= */

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    position: relative;
    z-index: 1;
}


/* =========================================================
   MAIN BACKGROUND
========================================================= */

.stApp {
    min-height: 100vh !important;

    background:
        radial-gradient(
            circle at 15% 20%,
            rgba(139, 92, 246, 0.35),
            transparent 25%
        ),
        radial-gradient(
            circle at 85% 30%,
            rgba(59, 130, 246, 0.25),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #050510 0%,
            #11113a 45%,
            #352080 100%
        ) !important;

    color: white !important;
}


/* =========================================================
   STARS
========================================================= */

.stApp::before {
    content: "✦   ·    ✧       ·   ✦     ·        ✧    ·   ✦";
    position: fixed;
    top: 5%;
    left: 5%;
    width: 90%;
    height: 90%;
    color: rgba(255,255,255,0.35);
    font-size: 18px;
    letter-spacing: 35px;
    line-height: 100px;
    pointer-events: none;
    z-index: 0;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #08081a 0%,
            #151044 100%
        ) !important;

    border-right: 1px solid rgba(255,255,255,0.10);
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: white !important;
}

.small-text {
    color: #aaa7c7 !important;
    font-size: 14px;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #ddd6fe !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}


/* =========================================================
   HERO
========================================================= */

.hero {
    padding: 45px 40px;
    border-radius: 28px;

    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(236,72,153,0.35),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            rgba(91,33,182,0.95),
            rgba(30,27,75,0.95)
        );

    border: 1px solid rgba(255,255,255,0.15);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.35);

    margin-top: 0;
    margin-bottom: 30px;

    overflow: hidden;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin: 0 0 10px 0;
    color: white !important;
}

.hero p {
    font-size: 19px;
    color: #ddd6fe !important;
    margin: 0;
}


/* =========================================================
   HEADINGS
========================================================= */

h1,
h2,
h3 {
    color: white !important;
}


/* =========================================================
   TEXT
========================================================= */

p {
    color: #ddd6fe;
}


/* =========================================================
   TEXT AREAS
========================================================= */

textarea {
    border-radius: 12px !important;

    background-color:
        rgba(10,10,30,0.90) !important;

    color: white !important;

    border:
        1px solid rgba(168,85,247,0.35) !important;
}

textarea::placeholder {
    color: #9ca3af !important;
}


/* =========================================================
   SELECT BOX
========================================================= */

div[data-baseweb="select"] > div {
    background-color:
        rgba(10,10,30,0.90) !important;

    border-radius: 12px !important;

    border:
        1px solid rgba(168,85,247,0.35) !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {
    border-radius: 12px !important;

    font-weight: 700 !important;

    border: none !important;

    padding: 12px;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #a855f7
        ) !important;

    color: white !important;

    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 25px
        rgba(168,85,247,0.50);
}


/* =========================================================
   DOWNLOAD BUTTON
========================================================= */

.stDownloadButton > button {
    border-radius: 12px !important;

    font-weight: 700 !important;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #a855f7
        ) !important;

    color: white !important;

    border: none !important;
}


/* =========================================================
   INFO BOX
========================================================= */

div[data-testid="stAlert"] {
    background-color:
        rgba(30,27,75,0.85) !important;

    border-radius: 12px !important;

    color: white !important;
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {
    border-color:
        rgba(255,255,255,0.12) !important;
}


/* =========================================================
   FOOTER
========================================================= */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# OLLAMA MODEL
# =========================================================

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.3
)


# =========================================================
# AI FUNCTIONS
# =========================================================

def generate_email(reason, template):

    prompt = f"""
You are an expert professional email writing assistant.

Create a complete professional email based on the user's situation.

Situation:
{reason}

Email type:
{template}

Requirements:
- Create a suitable subject.
- Use a polite greeting.
- Clearly explain the situation.
- Keep the email professional and natural.
- End with an appropriate closing.
- Do not add explanations outside the email.

Return only the final email.
"""

    response = llm.invoke(prompt)
    return response.content


def generate_reply(email):

    prompt = f"""
You are an intelligent professional email assistant.

The user received the following email:

{email}

Write an appropriate reply.

Requirements:
- Understand the message.
- Respond directly to the sender.
- Be polite and professional.
- Keep the reply concise but complete.
- Return only the reply email.
"""

    response = llm.invoke(prompt)
    return response.content


def improve_email(email):

    prompt = f"""
You are a professional email editor.

Improve the following email:

{email}

Requirements:
- Correct grammar.
- Improve sentence structure.
- Make it professional and clear.
- Keep the original meaning.
- Do not add unnecessary information.
- Return only the improved email.
"""

    response = llm.invoke(prompt)
    return response.content


def change_tone(email, tone):

    prompt = f"""
You are a professional email rewriting assistant.

Rewrite the following email using this tone:

Tone: {tone}

Original email:
{email}

Requirements:
- Keep the original meaning.
- Do not add false information.
- Make the tone clearly match the selected style.
- Return only the rewritten email.
"""

    response = llm.invoke(prompt)
    return response.content


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = ""

if "last_action" not in st.session_state:
    st.session_state.last_action = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📧 AI Email Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="small-text">Powered by Ollama + LangChain</p>',
        unsafe_allow_html=True
    )

    st.divider()

    feature = st.radio(
        "Choose a feature",
        [
            "✍️ Generate Email",
            "📩 Smart Reply",
            "✨ Improve Email",
            "🎭 Change Tone"
        ]
    )

    st.divider()

    st.markdown("### 🤖 AI Model")

    st.info(
        "Ollama\n\nModel: gemma3:1b"
    )

    st.markdown(
        '<p class="small-text">Runs locally on your computer.</p>',
        unsafe_allow_html=True
    )


# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">
<h1>📧 AI Email Assistant</h1>
<p>Write smarter emails with the help of local AI. Generate, reply, improve and customize your emails.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# GENERATE EMAIL
# =========================================================

if feature == "✍️ Generate Email":

    st.header("✍️ Generate a Professional Email")

    st.write(
        "Describe your situation and AI will create "
        "a professional email for you."
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        reason = st.text_area(
            "Describe your situation",
            placeholder=(
                "Example: I need two days leave because "
                "I have to attend a family function."
            ),
            height=180
        )

    with col2:

        template = st.selectbox(
            "Choose email type",
            [
                "General",
                "College Leave",
                "Job Application",
                "Meeting Request",
                "Apology",
                "Follow-up",
                "Permission Request"
            ]
        )

        st.write("")

        generate_button = st.button(
            "✨ Generate Email",
            use_container_width=True
        )

    if generate_button:

        if reason.strip() == "":
            st.warning("Please describe your situation.")

        else:

            with st.spinner(
                "🤖 AI is writing your email..."
            ):

                try:

                    result = generate_email(
                        reason,
                        template
                    )

                    st.session_state.result = result
                    st.session_state.last_action = "Generated Email"

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# SMART REPLY
# =========================================================

elif feature == "📩 Smart Reply":

    st.header("📩 Smart Reply")

    st.write(
        "Paste an email you received and AI "
        "will create a suitable reply."
    )

    email = st.text_area(
        "Paste the received email",
        placeholder="Paste the email here...",
        height=250
    )

    if st.button(
        "🤖 Generate Smart Reply",
        use_container_width=True
    ):

        if email.strip() == "":
            st.warning("Please paste an email.")

        else:

            with st.spinner(
                "🤖 AI is preparing your reply..."
            ):

                try:

                    result = generate_reply(email)

                    st.session_state.result = result
                    st.session_state.last_action = "Smart Reply"

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# IMPROVE EMAIL
# =========================================================

elif feature == "✨ Improve Email":

    st.header("✨ Improve Your Email")

    st.write(
        "Paste a rough email and AI will make "
        "it clearer and more professional."
    )

    email = st.text_area(
        "Your email",
        placeholder="Write or paste your email here...",
        height=250
    )

    if st.button(
        "✨ Improve Email",
        use_container_width=True
    ):

        if email.strip() == "":
            st.warning("Please enter an email.")

        else:

            with st.spinner(
                "🤖 AI is improving your email..."
            ):

                try:

                    result = improve_email(email)

                    st.session_state.result = result
                    st.session_state.last_action = "Improved Email"

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# CHANGE TONE
# =========================================================

elif feature == "🎭 Change Tone":

    st.header("🎭 Change Email Tone")

    st.write(
        "Rewrite your email according to the tone you want."
    )

    email = st.text_area(
        "Enter your email",
        placeholder="Paste your email here...",
        height=220
    )

    tone = st.selectbox(
        "Choose the tone",
        [
            "Formal",
            "Friendly",
            "Polite",
            "Concise"
        ]
    )

    if st.button(
        "🎭 Change Tone",
        use_container_width=True
    ):

        if email.strip() == "":
            st.warning("Please enter an email.")

        else:

            with st.spinner(
                f"🤖 Rewriting your email in a {tone.lower()} tone..."
            ):

                try:

                    result = change_tone(
                        email,
                        tone
                    )

                    st.session_state.result = result
                    st.session_state.last_action = f"{tone} Email"

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# OUTPUT SECTION
# =========================================================

if st.session_state.result:

    st.divider()

    st.subheader(
        f"✨ {st.session_state.last_action}"
    )

    st.text_area(
        "AI Output",
        value=st.session_state.result,
        height=350
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📥 Download Email",
            data=st.session_state.result,
            file_name="ai_email.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        if st.button(
            "🗑️ Clear Output",
            use_container_width=True
        ):

            st.session_state.result = ""
            st.session_state.last_action = ""

            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<center>
<p class="small-text">
📧 AI Email Assistant &nbsp; | &nbsp;
Python + Streamlit + LangChain + Ollama
</p>
</center>
""", unsafe_allow_html=True)
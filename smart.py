import streamlit as st
import google.generativeai as genai
import datetime

# 1. API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# 2. Page Config
st.set_page_config(page_title="Study Smart AI", page_icon="📚", layout="centered")

# 3. Sidebar - Dashboard
with st.sidebar:
    st.title("Project Dashboard")
    subject = st.selectbox(
        "Choose your Subject:",
        ("General Inquiry", "Geography", "History", "Chemistry", "Math", "Physics", "Biology")
    )
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- CUSTOM SUBJECT LOGIC ---
if subject == "Geography":
    instruction = "You are a Geography expert. Respond ONLY using this format: ck - [Facts], cu - [Explanation], ap - [Impact]. No intro chatter."
elif subject == "History":
    instruction = "You are a History expert. Respond ONLY using this format: hk - [Knowledge], hu - [Understanding], ht - [Thinking]. No intro chatter."
elif subject == "Chemistry":
    instruction = "You are a Chemistry manual. For industrial processes, ONLY use headers: 1. Title, 2. Introduction, 3. Raw Materials, 4. Procedures, 5. Side effects, 6. Social benefits. No intro chatter."
else:
    # This covers "General Inquiry", Math, etc.
    instruction = "You are a helpful, friendly assistant. Answer questions clearly and naturally without any special codes or numbered headers."

# AI Personality
model = genai.GenerativeModel(
    model_name='gemini-3.1-flash-lite-preview', 
    system_instruction=f"You are a helpful school study assistant specializing in {subject}. Analyze any images provided to help the student. Be encouraging and academic."
)

# 4. Header
st.markdown(f"# 📚 Study Smart AI: {subject}")
study_goal = st.text_input("What is your goal for this session?", placeholder="e.g., Just chatting or solving a specific problem")

# 5. Chat History Display
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Main Chat Input
if prompt := st.chat_input(f"Type your {subject} message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Subject Specific Forcing
    if subject == "Chemistry":
        final_query = f"INDUSTRIAL PROCESS: {prompt}. 6-point format only."
    elif subject == "Geography":
        final_query = f"{prompt}. Format: ck, cu, ap only."
    elif subject == "History":
        final_query = f"{prompt}. Format: hk, hu, ht only."
    else:
        # No forcing for General Inquiry or Math
        final_query = prompt

    try:
        response = model.generate_content(final_query)
        
        # Save to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

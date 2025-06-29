import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# --- Load API Key ---
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

set_tracing_disabled(disabled=True)

# --- Define the Agent Once ---
agent = Agent(
    name="CheckInBuddy",
    instructions="You're kind, warm, and helpful. Always validate the user's emotions.",
    model=OpenAIChatCompletionsModel(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        openai_client=client,
    )
)

# --- Async Function for Mood Analysis ---
async def analyze_mood(responses):
    joined_prompt = "\n".join([
        "You're a compassionate mental health assistant.",
        "Your job is to reflect kindly on the user's emotions, reassure them, and offer encouraging words.",
        f"1. How have you been feeling lately?\n{responses['q1']}",
        f"2. What's been on your mind?\n{responses['q2']}",
        f"3. How have your energy or sleep levels been?\n{responses['q3']}",
        f"4. Anything else they wanted to share?\n{responses.get('q4', '')}",
        "Kindly analyze how they might be feeling, reassure them with empathy, and let them know they're not alone. End with a gentle check-out message like 'I'm always here if you need to talk again.'"
    ])
    result = await Runner.run(agent, joined_prompt)
    return result.final_output

# --- Async Function for Follow-up ---
async def follow_up():
    follow_up_prompt = "Would you like to share anything else or continue the conversation?"
    result = await Runner.run(agent, follow_up_prompt)
    return result.final_output

# --- Streamlit UI ---
st.set_page_config(page_title="Mental Health Checker", page_icon="🧠")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #dfffe0;
    }
    [data-testid="stSidebar"] {
        background-color: #cdebc1;
    }
    div[data-testid="stMarkdownContainer"] {
        color: black;
    }
    .stButton > button {
        background-color: #E6E6FA;
        color: black;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #D8BFD8;
        color: white;
        transform: scale(1.05);
    }
    .ai-response {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        color: black;
    }
    img.avatar {
        width: 50px;
        vertical-align: middle;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Mental Health Mood Checker")
st.markdown("Let's reflect together. Your answers stay private.")

with st.form("mood_form"):
    q1 = st.text_area("1. How have you been feeling emotionally lately?")
    q2 = st.text_area("2. What’s been on your mind the most?")
    q3 = st.text_area("3. How have your energy or sleep levels been?")
    q4 = st.text_area("4. Would you like to share anything else? (optional)")
    submitted = st.form_submit_button("Check My Mood")

if submitted:
    with st.spinner("Analyzing your mood..."):
        responses = {"q1": q1, "q2": q2, "q3": q3, "q4": q4}
        mood_result = asyncio.run(analyze_mood(responses))

    st.success("Here's what I think:")
    st.markdown(f"""
    <div class="ai-response">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="avatar" />
        <div>{mood_result}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("📝 I want to share something more"):
        with st.spinner("Listening with care..."):
            follow_up_response = asyncio.run(follow_up())
        st.markdown(f"""
        <div class="ai-response">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="avatar" />
            <div>{follow_up_response}</div>
        </div>
        """, unsafe_allow_html=True)

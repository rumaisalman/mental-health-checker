# import streamlit as st
# import asyncio
# import os
# from dotenv import load_dotenv
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# # Load API key
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# client = AsyncOpenAI(
#     api_key=OPENROUTER_API_KEY,
#     base_url="https://openrouter.ai/api/v1"
# )

# set_tracing_disabled(disabled=True)

# async def analyze_mood(responses):
#     joined_prompt = "\n".join([
#         "You're a compassionate mental health assistant.",
#         "Your job is to reflect kindly on the user's emotions, reassure them, and offer encouraging words.",
#         f"1. How have you been feeling lately?\n{responses['q1']}",
#         f"2. What's been on your mind?\n{responses['q2']}",
#         f"3. How have your energy or sleep levels been?\n{responses['q3']}",
#         f"4. Anything else they wanted to share?\n{responses['q4']}",
#         "Kindly analyze how they might be feeling, reassure them with empathy, and let them know they're not alone. End with a gentle check-out message like 'I'm always here if you need to talk again.'"
#     ])

#     agent = Agent(
#         name="CheckInBuddy",
#         instructions="You're kind, warm, and helpful. Always validate the user's emotions.",
#         model=OpenAIChatCompletionsModel(
#             model="mistralai/mistral-small-3.2-24b-instruct:free",
#             openai_client=client,
#         )
#     )

#     result = await Runner.run(agent, joined_prompt)
#     return result.final_output

# # --- Streamlit UI ---
# st.set_page_config(page_title="Mental Health Checker", page_icon="💬")
# st.title("🧠 Mental Health Mood Checker")
# st.markdown("Let's reflect together. Your answers stay private.")

# with st.form("mood_form"):
#     q1 = st.text_area("1. How have you been feeling emotionally lately?")
#     q2 = st.text_area("2. What’s been on your mind the most?")
#     q3 = st.text_area("3. How have your energy or sleep levels been?")
#     q4 = st.text_area("4. Would you like to share anything else? (optional)")
#     submitted = st.form_submit_button("Check My Mood")

# if submitted:
#     with st.spinner("Analyzing your mood..."):
#         responses = {
#             "q1": q1,
#             "q2": q2,
#             "q3": q3,
#             "q4": q4  # <- this was missing and causing KeyError
#         }
#         mood_result = asyncio.run(analyze_mood(responses))
#         st.success("Here's what I think:")
#         st.markdown(f"💬 *{mood_result}*")

import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# Load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

set_tracing_disabled(disabled=True)

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

    agent = Agent(
        name="CheckInBuddy",
        instructions="You're kind, warm, and helpful. Always validate the user's emotions.",
        model=OpenAIChatCompletionsModel(
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            openai_client=client,
        )
    )

    result = await Runner.run(agent, joined_prompt)
    return result.final_output

# --- Streamlit UI ---
st.set_page_config(page_title="Mental Health Checker", page_icon="🧠")

# --- Custom CSS for soft styling ---
st.markdown("""
    <style>
    /* Change the background color of the main container */
    [data-testid="stAppViewContainer"] {
        background-color: #dfffe0;
    }

    /* Optional: Change sidebar background too */
    [data-testid="stSidebar"] {
        background-color: #cdebc1;
    }

    /* Text color for body content */
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
    </style>
""", unsafe_allow_html=True)


# --- Title & Form ---
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
        avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"

        st.markdown(f"""
<div class="ai-response" style="display: flex; align-items: flex-start;">
    <img src="{avatar_url}" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 10px;" />
    <div>{mood_result}</div>
</div>
""", unsafe_allow_html=True)

# Follow-up conversation option
follow_up = st.text_input("💬 Want to continue or share more?")

if follow_up:
    with st.spinner("Thinking..."):
        follow_up_prompt = f"""The user wants to continue the conversation after your mood analysis. Here's what they said:

        "{follow_up}"

        Kindly respond supportively, encourage them, and ask a gentle follow-up if appropriate."""
        
        follow_up_response = asyncio.run(Runner.run(agent, follow_up_prompt))
        
        st.markdown(f"""
        <div class="ai-response">
            <img src="{avatar_url}" class="avatar" />
            <div>{follow_up_response.final_output}</div>
        </div>
        """, unsafe_allow_html=True)

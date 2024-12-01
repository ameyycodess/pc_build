import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq  # Replace with the correct library if needed

# Load environment variables from the .env file
load_dotenv()

# Initialize the Groq client with the API key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),  # Ensure the key is set in .env
)

# Define a function to create a prompt for the chatbot
def create_prompt(message, context):
    return f"""
    You are a chatbot that helps users build a PC. Engage in a dialogue to guide the user through selecting compatible PC components based on their preferences and budget. Here is the context of the conversation so far:

    {context}

    User: {message}
    Chatbot:
    """

# Define a function to call the Groq API
def call_groq_api(prompt):
    try:
        # Create a chat completion using Groq's API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",  # Replace with the correct model name if needed
        )

        # Here, assuming that `chat_completion` is an object, you access the response as follows:
        # Check if `chat_completion` has an attribute "choices" and then extract the message content
        return chat_completion.choices[0].message.content.strip()  # Accessing the content correctly

    except Exception as e:
        # Handle any errors that occur during the API call
        return f"Error: {str(e)}"

# Initial context for the conversation
initial_context = "You are a chatbot that helps users build a PC."

# Function to handle the conversation flow
def chat_with_bot(user_message, context):
    prompt = create_prompt(user_message, context)
    response = call_groq_api(prompt)
    context += f"\nUser: {user_message}\nChatbot: {response}"
    return response, context

# Streamlit UI
st.title("PC Build Bot")
st.write("Hello! I am here to help you build your custom PC. Ask me anything!")

# Initialize session state
if "context" not in st.session_state:
    st.session_state.context = initial_context
if "responses" not in st.session_state:
    st.session_state.responses = []

# Capture user input (use st.session_state for persistence)
user_message = st.text_input("You:", value="", key="user_input")  # Do not set initial value from session state

# Button to send the message
if st.button("Send"):
    if user_message.strip():  # Ensure the message is not empty
        # Get the response from the bot and update the context
        response, st.session_state.context = chat_with_bot(user_message, st.session_state.context)
        st.session_state.responses.append((user_message, response))

# Display the conversation history
for user_message, response in st.session_state.responses:
    st.write(f"**You:** {user_message}")
    st.write(f"**Chatbot:** {response}")

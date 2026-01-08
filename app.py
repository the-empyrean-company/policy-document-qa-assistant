import gradio as gr
from openai import OpenAI

from config import OPENAI_API_KEY

# Initialise the OpenAI client using the key from config.py
client = OpenAI(api_key=OPENAI_API_KEY)


def chat_bot(message, history):
    """
    This is the function Gradio will call every time the user sends a message.

    - `message` is the latest user message (string).
    - `history` is a list of [user, assistant] pairs from the chat so far.
    """

    # Start with a system prompt to define the assistant behaviour
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Answer clearly and concisely."
            ),
        }
    ]

    # Add previous conversation turns from Gradio's history
    for user_message, assistant_message in history:
        if user_message:
            messages.append({"role": "user", "content": user_message})
        if assistant_message:
            messages.append({"role": "assistant", "content": assistant_message})

    # Add the latest user message
    messages.append({"role": "user", "content": message})

    # Call the OpenAI Chat Completions API
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # cheap, fast model suitable for a prototype
        messages=messages,
    )

    # Extract the assistant's reply text
    reply = response.choices[0].message.content
    return reply


# Build the Gradio interface
demo = gr.ChatInterface(
    fn=chat_bot,
    title="Policy / Document Q&A Assistant (Prototype)",
    description=(
        "Right now I am a general AI assistant. "
        "Later, I will be connected to your documents via RAG."
    ),
)


if __name__ == "__main__":
    demo.launch()

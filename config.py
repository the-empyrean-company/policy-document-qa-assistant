from dotenv import load_dotenv
import os

# Work out the absolute path to the folder this file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the full path to your .env file
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

# Load environment variables from that .env file
load_dotenv(dotenv_path=DOTENV_PATH)

# Read the OpenAI API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
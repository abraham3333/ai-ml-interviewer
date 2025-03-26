"""
AI-ML Code Interviewer - Main Application

This Streamlit application helps users prepare for machine learning and deep learning interviews by:
- Providing coding practice with adjustable difficulty levels
- Offering multiple-choice questions across various topics
- Generating explanations and feedback using Large Language Models
- Allowing configuration of LLM providers and settings

The application is designed to be modular and extensible, with separate components for:
- Coding practice
- Quiz generation
- Settings management
- Help documentation

Features:
- Code generation and evaluation
- Multiple-choice question generation
- Detailed explanations and feedback
- Configurable LLM providers (LM Studio, OpenAI, Anthropic, Google Gemini)
- Code execution control
- Session history tracking
"""
import logging
import os
import json

from config import config
import streamlit as st
from modules.coding_module import CodingModule
from dotenv import load_dotenv
from modules.help_module import HelpModule
from modules.llm_service import LLMService
from modules.quiz_module import QuizModule
from modules.settings_module import SettingsModule

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load settings from app.settings.json
with open("/content/ai-ml-code-interviewer/config/.app_settings.json", "r") as f:
    settings = json.load(f)

# Update config with settings from JSON file
config.LLM_PROVIDER = settings["llm_provider"]
config.LLM_BASE_URL = settings["llm_base_url"]
config.LLM_MODEL = settings["llm_model"]
config.LLM_TEMPERATURE = settings["llm_temperature"]
config.ENABLE_CODE_EXECUTION = settings["enable_code_execution"]
os.environ["GOOGLE_API_KEY"] = settings["google_api_key"]

def setup_page():
    """Set up the Streamlit page configuration."""
    st.set_page_config(
        page_title="ML/DL Interview Preparation",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Add custom CSS
    with open("styles/app.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def check_google_gemini_models():
    """
    Check if Google Gemini model is available and display appropriate message.
    """
    try:
        llm_service = LLMService(
            provider=config.LLM_PROVIDER,
            model=config.LLM_MODEL,
            base_url=config.LLM_BASE_URL,
            api_key=os.environ["GOOGLE_API_KEY"],
        )
        logger.info(f"Initialized LLM service with model: {config.LLM_MODEL}")
    except Exception as e:
        logger.error(f"Error initializing LLM service: {str(e)}")
        st.error("Failed to initialize LLM service. Please check your Google API key and try again.")
        st.stop()

def main():
    """Main application entry point."""
    # Set up the page
    setup_page()

    # Check Google Gemini model at startup
    if config.LLM_PROVIDER == "google":
        check_google_gemini_models()

    # App title and description
    st.title("Machine Learning & Deep Learning Interview Preparation")

    st.markdown(
        """
    This app helps you prepare for machine learning and deep learning interviews by providing:
    - **Coding Practice**: Implement ML/DL algorithms with adjustable difficulty
    - **Multiple Choice Questions**: Test your knowledge with ML/DL quizzes
    """
    )

    # Initialize modules
    coding_module = CodingModule()
    quiz_module = QuizModule()
    settings_module = SettingsModule()
    help_module = HelpModule()

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Coding Practice", "Multiple Choice Questions", "Settings", "Help"]
    )

    # Tab 1: Coding Practice
    with tab1:
        coding_module.render()

    # Tab 2: Multiple Choice Questions
    with tab2:
        quiz_module.render()

    # Tab 3: Settings
    with tab3:
        settings_module.render()

    # Tab 4: Help
    with tab4:
        help_module.render()

if __name__ == "__main__":
    main()

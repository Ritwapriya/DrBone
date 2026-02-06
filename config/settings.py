import os
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_PATH = "models/fracture.pt"
LOGO_PATH = "assets/logo.png"
FONT_PATH = "assets/Symbola.ttf"


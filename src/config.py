import os
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

# OpenAI compatible client setup for LLM (OpenRouter or NVIDIA or fallback to OpenAI)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM_BASE_URL = None
LLM_API_KEY = None
LLM_MODEL = "openai/gpt-4o-mini" # default openrouter model

if OPENROUTER_API_KEY:
    LLM_BASE_URL = "https://openrouter.ai/api/v1"
    LLM_API_KEY = OPENROUTER_API_KEY
elif NVIDIA_API_KEY:
    LLM_BASE_URL = "https://integrate.api.nvidia.com/v1"
    LLM_API_KEY = NVIDIA_API_KEY
    LLM_MODEL = "meta/llama-3.1-70b-instruct"
elif OPENAI_API_KEY:
    LLM_BASE_URL = "https://api.openai.com/v1"
    LLM_API_KEY = OPENAI_API_KEY
    LLM_MODEL = "gpt-4o-mini"

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

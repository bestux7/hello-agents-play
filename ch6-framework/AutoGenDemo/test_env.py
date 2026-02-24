import os
from dotenv import load_dotenv

load_dotenv()
print(f"model_id:{os.getenv('LLM_MODEL_ID')}")
print(f"base_url:{os.getenv('LLM_BASE_URL')}")
print(f"api_key:{os.getenv('LLM_API_KEY')}")
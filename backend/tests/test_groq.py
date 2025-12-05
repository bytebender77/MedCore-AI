import asyncio
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_settings
from app.core.llm_manager import LLMManager

async def test_groq():
    print("Testing Groq Integration...")
    settings = get_settings()
    llm = LLMManager(settings)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Groq is working!' if you can read this."}
    ]
    
    try:
        print(f"Sending request to Groq (Model: {settings.DEFAULT_GROQ_MODEL})...")
        response = await llm.generate(
            messages=messages,
            provider="groq",
            model=settings.DEFAULT_GROQ_MODEL
        )
        
        print("\nResponse received:")
        print("-" * 50)
        print(response["content"])
        print("-" * 50)
        print(f"Usage: {response['usage']}")
        print("SUCCESS: Groq integration verified.")
        
    except Exception as e:
        print(f"\nERROR: Groq test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_groq())

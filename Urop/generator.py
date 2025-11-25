import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


env_path = Path(__file__).resolve().parent / "API.env"
load_dotenv(env_path, override=True)

client = OpenAI()

def generate_code_baseline(prompt):
    """
    Baseline model: no retrieval.
    Returns ONLY python code, no explanation.
    """
    system_prompt = (
        "You are an expert Python programmer. "
        "Write ONLY runnable Python code. "
        "NO explanation, NO comments, NO markdown."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

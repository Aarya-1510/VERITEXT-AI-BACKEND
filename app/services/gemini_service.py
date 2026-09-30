import json
import time

from google import genai
from app.core.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_document(text: str):

    prompt = f"""
You are the AI analysis engine for a college project called VeriText AI.

Analyze the following document for possible plagiarism.

Important:
- Analyze the complete document.
- Identify sentences that appear copied, closely similar, or suspicious.
- Estimate an overall plagiarism percentage.
- For each sentence, provide a similarity percentage.
- Do not invent source URLs.
- If no reliable source is known, use null.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not add explanations outside the JSON.

Return exactly this structure:

{{
    "plagiarism_percentage": 0,
    "results": [
        {{
            "sentence": "Example sentence",
            "copied": false,
            "similarity": 0,
            "source": null
        }}
    ]
}}

DOCUMENT:

{text}
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
                
            )

            response_text = response.text.strip()

            response_text = response_text.replace(
                "```json", ""
            )
            response_text = response_text.replace(
                "```", ""
            )

            response_text = response_text.strip()

            return json.loads(response_text)

        except Exception as e:

            print(
                f"Gemini attempt {attempt + 1} failed: {e}"
            )

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                raise e
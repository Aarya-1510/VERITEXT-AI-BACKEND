from app.services.gemini_service import analyze_document


def check_plagiarism(text: str):

    if not text.strip():
        return {
            "plagiarism_percentage": 0,
            "results": []
        }

    try:

        result = analyze_document(text)

        return {
            "plagiarism_percentage": result.get(
                "plagiarism_percentage",
                0
            ),
            "results": result.get(
                "results",
                []
            )
        }

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "plagiarism_percentage": 0,
            "results": [],
            "error": str(e)
        }
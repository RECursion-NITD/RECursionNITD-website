import os
import requests
import json

def check_content_safety(text, title=None):
    """
    Checks if the provided text (and optional title) is safe using the Gemini API.
    Returns:
        - True: if content is safe
        - False: if content is unsafe
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    api_url = os.environ.get("GEMINI_API_URL")

    if not api_key or not api_url:
        print("Gemini API credentials missing in .env")
        return True # Fail open if not configured

    headers = {
        "Content-Type": "application/json"
    }
    
    # Append key to URL if not present (standard Gemini API pattern)
    if "?key=" not in api_url and "&key=" not in api_url:
        final_url = f"{api_url}?key={api_key}"
    else:
        final_url = api_url

    content_to_analyze = f"Title: {title}\n" if title else ""
    content_to_analyze += f"Body: {text}"

    prompt = f"""
    You are an AI Content Moderator for a college technical club website. Your goal is to filter user submissions for a Blog, Ask Section, Interview Experience Section. The environment must remain professional, academic, and safe.

    Analyze the input text (Title and Body) based on the following criteria:

    1. **SPAM & ADVERTISING (Strict Ban):**
    - Flag any promotion of pharmaceuticals, supplements, "useless medicines," weight loss pills, or male enhancement products.
    - Flag any commercial advertising, affiliate links, or "get rich quick" schemes.
    - Flag any text that looks like SEO spam (repetitive keywords without context).

    2. **SAFETY & TOXICITY (Strict Ban):**
    - Flag any sexual content, NSFW material, or innuendo.
    - Flag hate speech, harassment, or bullying.
    - Flag content encouraging self-harm or violence.

    3. **RELEVANCE (Allow):**
    - Allow questions about coding, engineering, science, and technology.
    - Allow general curiosity questions suitable for an academic environment.
    - Allow constructive discussions about college life or club activities.

    4. **TONE:**
    - The content must be professional or semi-professional.
    - Reject gibberish or incoherent text.

    Respond ONLY with a JSON object in the following format:
    {{
        "is_safe": true/false,
        "reason": "brief explanation if unsafe"
    }}

    Text to analyze:
    {content_to_analyze}
    """
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(final_url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Extract text response
        try:
            content_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Clean potential markdown formatting
            content_text = content_text.strip()
            if content_text.startswith("```json"):
                content_text = content_text[7:]
            if content_text.startswith("```"):
                content_text = content_text[3:]
            if content_text.endswith("```"):
                content_text = content_text[:-3]
            
            parsed = json.loads(content_text)
            return parsed.get("is_safe", True)
            
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Response body: {result}")
            return True # Fail open on parse error

    except Exception as e:
        print(f"Error checking content safety: {e}")
        return True # Fail open on network/API error

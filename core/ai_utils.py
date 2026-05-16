from google import genai
from django.conf import settings

def get_screening_agent_response(chat_history, skills_list):
    """
    Interacts with Gemini using the NEW google-genai library.
    """
    client = genai.Client(api_key=getattr(settings, 'GEMINI_API_KEY', ''))
    
    # Format history for the new library
    # The new library uses a slightly different structure than the old one
    formatted_history = []
    for msg in chat_history:
        # Convert role names if necessary
        role = msg['role']
        if role == 'model':
            role = 'model'
        
        formatted_history.append({
            "role": role,
            "parts": [{"text": msg['parts'][0]}]
        })

    system_prompt = f"""
    You are the LastBench Labs AI Screening Agent. 
    Your goal is to interview a candidate for specialized AI tasks.
    The candidate has selected these skills: {', '.join(skills_list)}.
    
    Guidelines:
    1. Evaluate English proficiency and communication clarity.
    2. Ask 1-2 deep technical questions for each skill mentioned.
    3. Be professional, encouraging, but rigorous.
    4. If the candidate gives a shallow answer, ask a follow-up.
    5. Keep the conversation to about 8-10 turns total.
    
    At the end of the interview (when you have enough info), 
    you must output a final evaluation in this EXACT format:
    [EVALUATION]
    Score: (0-100)
    Summary: (Short paragraph of strengths/weaknesses)
    Recommendation: (Verified / Not Recommended)
    [/EVALUATION]
    """
    
    # In the new library, we can pass system_instruction directly
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": system_prompt
        },
        history=formatted_history
    )
    
    response = chat.send_message("Continue the interview.")
    return response.text

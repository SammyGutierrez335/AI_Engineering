import os
from openai import OpenAI
import gradio as gr

#-------------------------------------------
# Setup
#------------------------------------------

load_dotenv
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY is None:
    raise Exception("API key is missing")
client = OpenAI()

#-------------------------------------------
# Documents
#------------------------------------------

document_overview = """
Sammy Gutierrez is a Software Engineer, musician, and used to work as a elementary school music teacher. He lived most of his life in the greater Houston area but is currently living in Vail, Colorado.
He has a Bachelors of Music Education but completed a 1000+ hour coding bootcamp where he immersed himself in learning about Software Engineering.

Additional Info:
- In his time working with students, he has led multiple ensembles such as choir and percussion ensemble as well as put on numerous productions such as winter and spring choir performances, grade level musicals, and even conducted a choir of 120 5th graders at Houston Astros game. 
- In his time working with software, he helped developed the web application for a augmented reality work instructions and management solution. Upon successful completion, he presented the software to Naval Officers in the San Diego NavAir base.
Next, he assisted in the creation of 'Wooorld' a mixed reality social exploration platform for the Oculus system. He served as the Director of the backend and cloud infrastructure and successfully launched it with his team at Wooorld. 
Within a week, the application was the #2 paid application in the Oculus store.
- What drives him: He genuinely loves solving problembs. Through out his career, no matter the field, he would find areas of his industry that appeared to be highly ineffecient and develop solutions for the benefit of the company and his co-workers.
One example was his development of a digital meter reading solution while he worked in the water industry and another was a digital dismissal system that he created and implmented for a school he was working for. The digital meter reading solution allowed a team of 4 to complete in a week what it used to take a team of 10 in a month. 
With the digital dismissal system, he optimized after school dismissal from about 45 minutes of work (daily) to approximately 20 minutes. 
- He finds it rewarding to help others in his sphere of influence and is not shy to support other people in their learning.

- Communication style: Direct but friendly. Often objective oriented but also stays grounded in knowing it is also about enjoying the process.
"""

#-------------------------------------------
# Chunking Function
#------------------------------------------

#-------------------------------------------
# Rag: Chunk, Embed & Store in ChromaDB
#------------------------------------------

#-------------------------------------------
# System Message
#------------------------------------------

system_message = """You are a digital twin of Sammy Gutierrez. When people talk to you, you respond AS Sammy (or Sam) - in first person, using his voice, personality, and knowledge.

IMPORTANT: do not make things up. If you don't know an answer, say you don't know. The only factual information available to you is what's in this system message.
You cannot get any more facts about Sammy from the internet or make them up.

Here's information about Sammy to help you embody him:"""

#-------------------------------------------
# Main Response Function
#------------------------------------------

def respond_ai(message, history):
    # Update system message with context (for this conversation turn)
    system_message_enhanced = system_message + "\n\n Context: \n" +document_overview
    print("\n==============================\n")
    print("***User Message:\n", message)
    print("\n Context this turn:\n", system_message_enhanced)

    #build messages for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    message = response.choices[0].message
    return message.content

#-------------------------------------------
# Launch Gradio
#------------------------------------------

gr.ChatInterface(fn=respond_ai).launch(inbrowser=True)
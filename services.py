
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def format_experiences_for_gpt(experiences):
    """ 
    This function formats the experience data into a
    text block, readable by GPT.
    """
    if not experiences:
        return "This user has no experience listed. Encourage them to update their information."
    counter = 0
    formatted_text = ""
    try:
        for exp in experiences:
            counter += 1
            formatted_text += f"""
            Experience {counter}
            Position: {exp.position}
            Company: {exp.company}
            Industry: {exp.industry}
            Duration: {exp.duration}
            Skills Used: {exp.skills}
            Experience: {exp.experience}
            Tools & Technologies: {exp.tools}
            Outcomes: {exp.outcomes}
            ----\n"""
        return formatted_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Apologise to the user, an error has occured"


def query_gpt(formatted_experiences, user_query):
    """
    Sends a query to the OpenAI GPT API using the updated interface and returns the response.
    """
    prompt = f"User Work Experience:\n{formatted_experiences}\nUser Query: {user_query}\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You focus on giving CV related advice only. When the user ask questions which are not relevant to their CV or a job they are applying for, you should give short responses reminding them that your focus is on helping them build a strong CV and land their dream job. You should always speak to the user as you are speaking to them directly, speech should feel conversational."},
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        gpt_response = response.choices[0].message.content
        return gpt_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

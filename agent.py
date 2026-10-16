import os
import sys
from dotenv import load_dotenv
from google import genai
import calculator as calc
from google.genai import types

load_dotenv()

def calculate(expression:str)->str:
    """Evaluate an arithmetic expression such as '15/270*20 + 6.
    Supports + - / * // % ** and parenthesis. 
    """
    try:
        return str(calc.calculate(expression))
    except ValueError as e:
        return f"Error: {e}"

client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def main():
    if len(sys.argv)<2:
        print('Usage python agent.py "<question>')
        sys.exit(2)
    question =" ".join(sys.argv[1:])
    response=client.models.generate_content(
        model="gemini-3.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction="You are a calculator assistant. If the question is not an arithmetic problem, or you cannot work out.",
            max_output_tokens=2000,
            tools=[calculate],
        )
    )
    print(response.text)

if __name__ =="__main__":
    main()
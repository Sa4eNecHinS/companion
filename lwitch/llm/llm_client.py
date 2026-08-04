import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

api_key = os.environ.get("API_KEY")
base_url = os.environ.get("BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def ask_llm(user_input: str) -> str | None:
    if not user_input:
        return None

    try:
        response = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error in function 'ask_llm' - {e}")
        return


if __name__ == "__main__":
    prompt = "Decribe me gpt-oss-120b model with only 2 sentences"
    print(ask_llm(prompt))

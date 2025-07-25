from restack_ai.function import function, log
from openai import OpenAI
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FunctionInputParams:
    user_content: str
    system_content: str | None = None
    model: str | None = None

@function.defn()
async def llm(input: FunctionInputParams) -> str:
    try:
        log.info("llm function started", input=input)
        client = OpenAI(base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY"))

        messages = []
        if input.system_content:
            messages.append({"role": "system", "content": input.system_content})
        messages.append({"role": "user", "content": input.user_content})

        response = client.chat.completions.create(
            model=input.model or "gpt-4o-mini",
            messages=messages
        )
        log.info("llm function completed", response=response)
        return response.choices[0].message.content
    except Exception as e:
        log.error("llm function failed", error=e)
        raise e

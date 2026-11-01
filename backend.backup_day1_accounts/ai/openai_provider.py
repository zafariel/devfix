import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenAIProvider:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não encontrada."
            )

        self.client = OpenAI(api_key=api_key)

    def ask(self, message, context=None):
        prompt = message

        if context:
            prompt = f"""
Você é o assistente do DEVFIX, uma ferramenta de diagnóstico de sites.

Use o diagnóstico abaixo como contexto para responder ao usuário.

DIAGNÓSTICO:
{context}

PERGUNTA DO USUÁRIO:
{message}
"""

        response = self.client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

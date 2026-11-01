import os
import json

from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()


class ClaudeProvider:
    def __init__(self):
        api_key = os.getenv("CLAUDE_API_KEY")

        if not api_key:
            raise RuntimeError(
                "CLAUDE_API_KEY não encontrada."
            )

        self.client = Anthropic(api_key=api_key)

    def comment_checks(self, issues):
        if not issues:
            return []

        payload = []

        for issue in issues:
            payload.append({
                "check": issue.get("check"),
                "message": issue.get("message"),
                "type": issue.get("type"),
                "severity": issue.get("severity"),
                "category": issue.get("category"),
                "problem": issue.get("problem"),
                "recommendation": issue.get("recommendation"),
            })

        prompt = f"""
Você é o especialista de IA do DEVFIX.

O DEVFIX possui checks determinísticos para diagnosticar sites.
Sua função NÃO é alterar o resultado dos checks.

Para cada check abaixo, escreva um comentário curto, claro e técnico
explicando por que aquele problema importa e o que o desenvolvedor
deve observar.

Retorne SOMENTE um JSON válido neste formato:

[
  {{
    "check": 1,
    "comment": "comentário..."
  }}
]

CHECKS:
{json.dumps(payload, ensure_ascii=False)}
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = response.content[0].text.strip()

        return json.loads(text)

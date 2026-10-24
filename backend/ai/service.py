from backend.ai.openai_provider import OpenAIProvider
from backend.ai.claude_provider import ClaudeProvider


class AIService:
    def __init__(self):
        self.openai = OpenAIProvider()
        self.claude = ClaudeProvider()

    def ask_chat(self, message, context=None):
        return self.openai.ask(
            message=message,
            context=context
        )

    def comment_checks(self, issues):
        return self.claude.comment_checks(issues)

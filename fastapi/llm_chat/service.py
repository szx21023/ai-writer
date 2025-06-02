from main import app

class LlmChatService:
    @staticmethod

    async def get_completion(prompt: str):
        completion = app.state.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message
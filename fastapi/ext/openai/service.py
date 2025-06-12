from main import app

class OpenaiService:
    @staticmethod
    async def get_completion(prompt: str):
        app.logger.info(f"Generating completion for prompt: {prompt}")
        completion = app.state.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip() if completion.choices else None
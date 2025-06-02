from openai import OpenAI

async def init_app(app):
    app.state.llm_client = OpenAI(
        api_key=app.state.config.get("OPENAI_API_KEY")
    )

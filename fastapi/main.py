from fastapi_basic.base_factory import BaseFactory

from database import engine, Base
from version import version
from conversation import init_app as init_conversation_app
from ext.openai import init_app as init_openai_app
from node import init_app as init_node_app

class AppFactory(BaseFactory):
    def get_app_config(self):
        from config import Config

        config = Config()
        return config.dict()

    def create_app(self):
        app = super().create_app()

        @app.on_event("startup")
        async def initail_app():
            await init_conversation_app(app)
            await init_node_app(app)

            app.state.llm_client = await init_openai_app(app)

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        @app.get("/hello")
        async def hello():
            from ext.openai.service import OpenaiService

            prompt = "英文的你好嗎怎麼說?"
            result = await OpenaiService.get_completion(prompt)
            print(result)

            return {
                'data': {
                    'version': version
                }
            }

        return app

app = AppFactory().create_app()
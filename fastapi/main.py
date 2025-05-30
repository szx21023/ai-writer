from fastapi_basic.base_factory import BaseFactory

from version import version

class AppFactory(BaseFactory):
    def get_app_config(self):
        return {}

    def create_app(self):
        app = super().create_app()

        @app.get("/hello")
        async def hello():
            return {
                'data': {
                    'version': version
                }
            }

        return app

app = AppFactory().create_app()
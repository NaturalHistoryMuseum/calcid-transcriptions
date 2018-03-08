from wsgicors import CORS

from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp
from apistar.backends import sqlalchemy_backend
from apistar.components.console import PrintConsole
from apistar import environment, typesystem


from api.model import Base
from api import routes


console = PrintConsole()


class Env(environment.Environment):
    properties = {
        'DEBUG': typesystem.boolean(default=False),
        'DATABASE_URL': typesystem.string()
    }

env = Env()


transcription_routes = [
    Route('/', 'GET', routes.get_unvalidated_transcription),
    Route('/export', 'GET', routes.export_validated_transcriptions_as_csv),
    Route('/', 'POST', routes.create_validated_transcription)
]

routes = [
    Include('/transcription', transcription_routes)
]


# Configure database settings.
settings = {
    "DATABASE": {
        "URL": env['DATABASE_URL'],
        "METADATA": Base.metadata
    },
}


class App(WSGIApp):

    def __call__(self, environ, start_response):
        cors = CORS(super().__call__, headers='*',
                    methods='*', origin='*')
        return cors(environ, start_response)


app = App(
    routes=routes,
    settings=settings,
    commands=sqlalchemy_backend.commands,  # Install custom commands.
    components=sqlalchemy_backend.components  # Install custom components.
)


if __name__ == '__main__':
    app.main()

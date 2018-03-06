import json
from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.backends import sqlalchemy_backend
from apistar.backends.sqlalchemy_backend import Session

from api.model import Base, RawTranscription


def get_transcription(session: Session):
    transcription = session.query(RawTranscription).first()
    return json.dumps(transcription)


def create_transcription():
    pass
    # if name is None:


def edit_transcription(transcription_id):
    pass
    # if name is None:
    #     return {'message': 'Welcome to API Star!'}
    # return {'message': 'Welcome to API Star, %s!' % name}

transcription_routes = [
    Route('/', 'GET', get_transcription),
    Route('/', 'POST', create_transcription),
    Route('/{transcription_id}', 'PUT', edit_transcription)
]


routes = [
    Include('/transcriptions', transcription_routes)
]


# Configure database settings.
settings = {
    "DATABASE": {
        "URL": "postgresql://:@localhost/mlm_transcriptions",
        "METADATA": Base.metadata
    }
}

app = App(
    routes=routes,
    settings=settings,
    commands=sqlalchemy_backend.commands,  # Install custom commands.
    components=sqlalchemy_backend.components  # Install custom components.
)


if __name__ == '__main__':
    app.main()

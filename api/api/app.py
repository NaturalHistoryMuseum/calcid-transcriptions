from wsgicors import CORS
import io
import csv

from apistar.backends.sqlalchemy_backend import Session

from apistar import http
from apistar import Include, Route, Response
from apistar.frameworks.wsgi import WSGIApp
from apistar.backends import sqlalchemy_backend
from apistar.components.console import PrintConsole


from api import db
from api.model import Base
from api.response import stream_csv


console = PrintConsole()


def create_validated_transcription(session: Session, request_data: http.RequestData):

    try:
        db.create_validated_transcription(session, request_data)
    except Exception:
        return Response(status=500)
    return {}


def get_unvalidated_transcription(session: Session):
    result = db.get_unvalidated_transcription(session)
    stats_result = db.get_validation_stats(session)
    return {
        'transcription': result.RawTranscription.as_dict(),
        'stats': {
            'total': stats_result.total,
            'validated': stats_result.validated
        },
        'multimedia': result.identifier
    }


def export_validated_transcriptions_as_csv(session: Session):

    transcriptions = db.get_all_validated_transcriptions(session)
    headers = transcriptions[0].as_dict().keys()
    rows = [t.as_dict().values() for t in transcriptions]
    return stream_csv(headers, rows)


transcription_routes = [
    Route('/', 'GET', get_unvalidated_transcription),
    Route('/export', 'GET', export_validated_transcriptions_as_csv),
    Route('/', 'POST', create_validated_transcription)
]

routes = [
    # Route('/export', 'GET', ),
    Include('/transcription', transcription_routes)
]


# Configure database settings.
settings = {
    "DATABASE": {
        "URL": "postgresql://:@localhost/mlm_transcriptions",
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

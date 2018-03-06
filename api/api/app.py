from wsgicors import CORS

# import sqlalchemy
from sqlalchemy import func

from apistar import http
from apistar import Include, Route, Response
from apistar.frameworks.wsgi import WSGIApp
from apistar.backends import sqlalchemy_backend
from apistar.backends.sqlalchemy_backend import Session
from apistar.components.console import PrintConsole

from api.model import Base, RawTranscription, ValidatedTranscription


console = PrintConsole()


def get_transcription(session: Session):
    transcription = session.query(RawTranscription).outerjoin(
        ValidatedTranscription).filter(ValidatedTranscription.subject_id == None).order_by(RawTranscription.subject_id).first()

    return {
        'record': transcription.as_dict(),
        'stats': get_stats(session)
    }


def create_corrected_transcription(session: Session, request_data: http.RequestData):

    try:
        validated_transcription = ValidatedTranscription(**request_data)
        session.add(validated_transcription)
        # Flush the changes to the database. This will populate the customer
        # id.
        session.flush()
    except Exception:
        return Response(status=500)
    return {}


def get_stats(session: Session):
    # select count(*) as total, count(v.subject_id) as validated from raw r
    # left join validated v on v.subject_id = r.subject_id;
    stats = session.query(
        func.count(RawTranscription.subject_id).label("total"),
        func.count(ValidatedTranscription.subject_id).label("validated")
    ).outerjoin(
        ValidatedTranscription).first()

    return {'total': stats.total, 'validated': stats.validated}

transcription_routes = [
    Route('/', 'GET', get_transcription),
    Route('/stats', 'GET', get_stats),
    Route('/', 'POST', create_corrected_transcription)
]

routes = [
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
                    methods='*', maxage='0', origin='*')
        return cors(environ, start_response)


app = App(
    routes=routes,
    settings=settings,
    commands=sqlalchemy_backend.commands,  # Install custom commands.
    components=sqlalchemy_backend.components  # Install custom components.
)


if __name__ == '__main__':
    app.main()

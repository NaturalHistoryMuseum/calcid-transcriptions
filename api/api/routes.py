
from apistar.backends.sqlalchemy_backend import Session
from apistar import Response
from apistar import http


from api import db
from api.response import stream_csv


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

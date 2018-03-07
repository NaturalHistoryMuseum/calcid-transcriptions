from sqlalchemy import func

from apistar.backends.sqlalchemy_backend import Session

from api.model import RawTranscription, ValidatedTranscription, Multimedia


def get_unvalidated_transcription(session: Session):
    return session.query(RawTranscription, Multimedia.identifier).outerjoin(
        ValidatedTranscription).join(Multimedia).filter(ValidatedTranscription.subject_id == None).order_by(RawTranscription.subject_id).first()


def create_validated_transcription(session: Session, data):

    validated_transcription = ValidatedTranscription(**data)
    session.add(validated_transcription)
    # Flush the changes to the database. This will populate the customer
    # id.
    session.flush()


def get_validation_stats(session: Session):
    # select count(*) as total, count(v.subject_id) as validated from raw r
    # left join validated v on v.subject_id = r.subject_id;
    stats = session.query(
        func.count(RawTranscription.subject_id).label("total"),
        func.count(ValidatedTranscription.subject_id).label("validated")
    ).outerjoin(
        ValidatedTranscription).first()
    return stats


def get_all_validated_transcriptions(session: Session):
    return session.query(ValidatedTranscription).all()

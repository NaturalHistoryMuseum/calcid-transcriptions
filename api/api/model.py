import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey


Base = declarative_base()


from apistar.components.console import PrintConsole
console = PrintConsole()


class TranscriptionMixin(object):
    combidate = Column(String)
    endcombidate = Column(String)
    country = Column(String)
    collector1 = Column(String)
    collector2 = Column(String)
    host_insect = Column(String)
    host_plant = Column(String)
    registration_number = Column(String)
    is_uncertainty = Column(Boolean)
    is_type = Column(String)
    subject_catalogue_irn = Column(Integer)
    note = Column(String)
    type_status = Column(String)

    def as_dict(self):
        return {c.name: self._encode_value(getattr(self, c.name)) for c in self.__table__.columns}

    @staticmethod
    def _encode_value(value):
        # If it's a date, format it, otherwise return string (is not None)
        if not value:
            return value
        elif type(value) is datetime.datetime:
            return value.strftime("%H:%M %d %b %Y")
        else:
            return str(value)


class RawTranscription(TranscriptionMixin, Base):
    subject_id = Column(Integer, primary_key=True)
    __tablename__ = "raw"


class ValidatedTranscription(TranscriptionMixin, Base):
    subject_id = Column(ForeignKey(
        RawTranscription.subject_id), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    __tablename__ = "validated"


class Multimedia(Base):
    subject_id = Column(ForeignKey(
        RawTranscription.subject_id), primary_key=True)
    identifier = Column(String)

    __tablename__ = "multimedia_identifiers"

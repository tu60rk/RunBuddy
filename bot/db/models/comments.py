from datetime import date
from sqlalchemy import Uuid, text, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from db import Base
from .registration import Registration


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_telegram: Mapped[UUID] = mapped_column(String(255), ForeignKey("registration.id_telegram"), nullable=False, unique=True)
    date_comment: Mapped[date] = mapped_column(Date, nullable=False)
    comment: Mapped[date] = mapped_column(String(255))

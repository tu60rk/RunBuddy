from datetime import date
from sqlalchemy import Uuid, text, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from db import Base


class Meets(Base):
    __tablename__ = "meets"

    id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_first_partner: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("registration.id"), nullable=False
    )
    id_second_partner: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("registration.id"), nullable=False
    )
    date_algorithm: Mapped[date] = mapped_column(Date, nullable=False)
    first_partner_meet: Mapped[bool] = mapped_column(Boolean)
    second_partner_meet: Mapped[bool] = mapped_column(Boolean)

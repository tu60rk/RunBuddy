from sqlalchemy import String, Integer, Boolean, Uuid, text
from sqlalchemy.dialects.postgresql import UUID as alcUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from db import Base


class Registration(Base):
    __tablename__ = "registration"

    # id: Mapped[UUID] = mapped_column(alcUUID(as_uuid=True), primary_key=True)

    id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_name: Mapped[str] = mapped_column(String(250), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    sex: Mapped[str] = mapped_column(String(7), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    run_level: Mapped[str] = mapped_column(String(8), nullable=False)
    account_link: Mapped[str] = mapped_column(String(255))
    level_partner_need: Mapped[bool] = mapped_column(Boolean, nullable=False)
    any_gender: Mapped[bool] = mapped_column(Boolean, nullable=False)
    meet_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_telegram: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(50))
    link_telegram: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # relate_first_partner = relationship("Meets")
    # relate_second_partner = relationship("Meets")

    # relate_first_partner = relationship("Meets", back_ref="meets_first", foreign_keys=["Meets.id_first_partner"])
    # relate_second_partner = relationship("Meets", back_ref="meets_second", foreign_keys=["Meets.id_second_partner"])
    # meets_first_partner: Mapped[list["Meets"]] = relationship(back_populates="registration", foreign_keys=["Meets.id_first_partner"])
    # meets_second_partner: Mapped[list["Meets"]] = relationship(back_populates="registration", foreign_keys=["Meets.id_second_partner"])

    # def __repr__(self) -> str:
    #     name = f"{self.nick_name} {self.name}"
    #     return f"[{self.id_telegram}] {name}"

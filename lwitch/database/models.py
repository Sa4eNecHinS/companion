from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Dialogue(Base):
    __tablename__ = "dialogues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    user_input: Mapped[str] = mapped_column(Text, nullable=False)
    sanitized_user_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    block_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    llm_response: Mapped[str | None] = mapped_column(Text, nullable=True)

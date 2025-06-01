"""Models."""

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

engine = create_engine("sqlite:///src/database.db")


class User(SQLModel, table=True):
    """User model."""

    id: int = Field(
        default=None,
        primary_key=True,
    )
    phone_number: str = Field(
        index=True,
        unique=True,
        nullable=False,
        max_length=15,
    )
    age: int
    notice: str = Field(
        default=None,
        nullable=True,
    )

    @classmethod
    def check_user_exists(
        cls,
        phone_number: str,
    ) -> bool:
        """Check if a user exists by phone number."""
        with Session(engine) as session:
            result = session.exec(
                select(cls).where(cls.phone_number == phone_number),
            ).first()
            return result is not None

    @classmethod
    def create_user(
        cls,
        phone_number: str,
        age: int,
        notice: Optional[str] = None,
    ) -> "User":
        """Create a new user."""
        with Session(engine) as session:
            # check if user already exists
            user = session.exec(
                select(cls).where(cls.phone_number == phone_number),
            ).first()
            if user:
                return user
            user = cls(phone_number=phone_number, age=age, notice=notice)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user


SQLModel.metadata.create_all(engine)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        class_name = cls.__name__
        tablename = ""

        for idx, ch in enumerate(class_name):
            if idx and ch.isupper():
                ch = f"_{ch}"
            tablename += ch.lower()

        parts = tablename.split("_")

        if len(parts) == 1:
            return tablename + "s"

        parts = [part + "s" for part in parts]
        return "_".join(parts)

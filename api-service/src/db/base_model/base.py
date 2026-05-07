from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Provides common functionality:
    - Declarative base for model definition
    - Custom __repr__ for debugging

    Attributes:
        repr_cols: Explicit columns to include in repr.
        repr_cols_num: Number of first columns to include in repr.
    """

    repr_cols = ()
    repr_cols_num = 3

    def __repr__(self):
        """
        String representation of the model.

        Includes column names and values for debugging.

        Returns:
            String in format "<ClassName col1=val1, col2=val2, ...>".
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

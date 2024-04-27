from datetime import date, datetime

import sqlalchemy.orm as so

from src.core.models import Base
from src.core.schemas import SpimexTradingResults as SpimexTradingResultsSchema


class SpimexTradingResults(Base):
    __tablename__ = "spimex_trading_results"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    exchange_product_id: so.Mapped[str]
    exchange_product_name: so.Mapped[str]
    oil_id: so.Mapped[str]
    delivery_basis_id: so.Mapped[str]
    delivery_basis_name: so.Mapped[str]
    delivery_type_id: so.Mapped[str]
    volume: so.Mapped[str]
    total: so.Mapped[str]
    count: so.Mapped[str]
    date: so.Mapped[date]
    created_on: so.Mapped[datetime] = so.mapped_column(default=datetime.now)
    updated_on: so.Mapped[datetime] = so.mapped_column(default=datetime.now, onupdate=datetime.now)

    def to_pydantic_schema(self) -> SpimexTradingResultsSchema:
        return SpimexTradingResultsSchema(
            id=self.id,
            exchange_product_id=self.exchange_product_id,
            exchange_product_name=self.exchange_product_name,
            oil_id=self.oil_id,
            delivery_basis_id=self.delivery_basis_id,
            delivery_basis_name=self.delivery_basis_name,
            delivery_type_id=self.delivery_type_id,
            volume=self.volume,
            total=self.total,
            count=self.count,
            date=self.date,
            created_on=self.created_on,
            updated_on=self.updated_on,
        )

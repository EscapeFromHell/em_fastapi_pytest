from datetime import date, datetime
from src.core.schemas import SpimexTradingResults

FAKE_TRADING_RESULTS: list[SpimexTradingResults] = [
    SpimexTradingResults(
        id=1,
        exchange_product_id="exchange_product_id_1",
        exchange_product_name="exchange_product_name_1",
        oil_id="oil_id_1",
        delivery_basis_id="delivery_basis_id_1",
        delivery_basis_name="delivery_basis_name_1",
        delivery_type_id="delivery_type_id_1",
        volume="volume_1",
        total="total_1",
        count="count_1",
        date=date(2024, 4, 25),
        created_on=datetime(2024, 4, 25, 10, 10, 10, 0),
        updated_on=datetime(2024, 4, 25, 10, 10, 10, 0)

    ),
    SpimexTradingResults(
        id=2,
        exchange_product_id="exchange_product_id_2",
        exchange_product_name="exchange_product_name_2",
        oil_id="oil_id_2",
        delivery_basis_id="delivery_basis_id_2",
        delivery_basis_name="delivery_basis_name_2",
        delivery_type_id="delivery_type_id_2",
        volume="volume_2",
        total="total_2",
        count="count_2",
        date=date(2024, 4, 24),
        created_on=datetime(2024, 4, 24, 10, 10, 10, 0),
        updated_on=datetime(2024, 4, 24, 10, 10, 10, 0)
    ),
    SpimexTradingResults(
        id=3,
        exchange_product_id="exchange_product_id_3",
        exchange_product_name="exchange_product_name_3",
        oil_id="oil_id_3",
        delivery_basis_id="delivery_basis_id_3",
        delivery_basis_name="delivery_basis_name_3",
        delivery_type_id="delivery_type_id_3",
        volume="volume_3",
        total="total_3",
        count="count_3",
        date=date(2024, 4, 23),
        created_on=datetime(2024, 4, 23, 10, 10, 10, 0),
        updated_on=datetime(2024, 4, 23, 10, 10, 10, 0)
    ),
]
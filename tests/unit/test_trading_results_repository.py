from datetime import date

import pytest

from src.core.db import async_session as async_db_session
from src.core.models import SpimexTradingResults
from src.core.repository import TradingResultsRepository
from tests.fakes import FAKE_TRADING_RESULTS


class TestRepo:
    @pytest.mark.parametrize(
        "date, expected_result", [(date(2024, 4, 25), FAKE_TRADING_RESULTS[0]), (date(2024, 4, 26), None)]
    )
    @pytest.mark.asyncio
    async def test_fetch_one_trading_result_by_date(
        self, clean_trading_results, add_trading_results, async_session_maker, date, expected_result
    ):
        async with async_db_session() as session:
            repo = TradingResultsRepository(session=session)
            await clean_trading_results()
            await add_trading_results()
            result = await repo.fetch_one_trading_result_by_date(date=date)
            if result:
                result = result.to_pydantic_schema()
            assert result == expected_result
            await session.close()

    @pytest.mark.asyncio
    async def test_add_all_to_db(self, get_trading_results, clean_trading_results):
        async with async_db_session() as session:
            repo = TradingResultsRepository(session=session)
            await clean_trading_results()
            objects = []
            for trading_result in FAKE_TRADING_RESULTS:
                trading_result = trading_result.model_dump()
                objects.append(SpimexTradingResults(**trading_result))
            await repo.add_all_to_db(objects=objects)
            results = await get_trading_results()
            assert len(results) == len(FAKE_TRADING_RESULTS)

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, expected_result",
        [(None, None, None, [FAKE_TRADING_RESULTS[0]]), ("A100", None, None, [])],
    )
    @pytest.mark.asyncio
    async def test_get_last_results(
        self, clean_trading_results, add_trading_results, oil_id, delivery_type_id, delivery_basis_id, expected_result
    ):
        async with async_db_session() as session:
            repo = TradingResultsRepository(session=session)
            await clean_trading_results()
            await add_trading_results()
            result = await repo.get_last_results(
                oil_id=oil_id, delivery_type_id=delivery_type_id, delivery_basis_id=delivery_basis_id
            )
            if result:
                result = [result.to_pydantic_schema() for result in result]
            assert result == expected_result
            await session.close()

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, start_date, end_date, expected_result",
        [
            (None, None, None, date(2024, 4, 24), date(2024, 4, 25), FAKE_TRADING_RESULTS[:2]),
            ("A100", None, None, date(2024, 4, 24), date(2024, 4, 25), []),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_trading_results_in_period(
        self,
        clean_trading_results,
        add_trading_results,
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        start_date,
        end_date,
        expected_result,
    ):
        async with async_db_session() as session:
            repo = TradingResultsRepository(session=session)
            await clean_trading_results()
            await add_trading_results()
            result = await repo.get_trading_results_in_period(
                oil_id=oil_id,
                delivery_type_id=delivery_type_id,
                delivery_basis_id=delivery_basis_id,
                start_date=start_date,
                end_date=end_date,
            )
            if result:
                result = [result.to_pydantic_schema() for result in result]
            assert result == expected_result
            await session.close()

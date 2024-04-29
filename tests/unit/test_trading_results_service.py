from datetime import date

import pytest

from src.core.schemas import LastTradingDates, TradingResultsList
from src.core.service import TradingResultsService
from src.core.uow import UnitOfWork
from tests.fakes import FAKE_TRADING_RESULTS


class TestService:
    @pytest.mark.parametrize(
        "days, expected_result",
        [
            (365, LastTradingDates(last_trading_dates=[date(2024, 4, 25), date(2024, 4, 24), date(2024, 4, 23)])),
            (1, LastTradingDates(last_trading_dates=[])),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_last_trading_dates(self, clean_trading_results, add_trading_results, days, expected_result):
        await clean_trading_results()
        await add_trading_results()
        result = await TradingResultsService.get_last_trading_dates(uow=UnitOfWork(), days=days)
        assert result == expected_result

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, expected_result",
        [
            (None, None, None, TradingResultsList(trading_results=[FAKE_TRADING_RESULTS[0]])),
            (
                "oil_id_1",
                "delivery_type_id_1",
                "delivery_basis_id_1",
                TradingResultsList(trading_results=[FAKE_TRADING_RESULTS[0]]),
            ),
            ("A100", None, None, TradingResultsList(trading_results=[])),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_last_trading_results(
        self, add_trading_results, clean_trading_results, oil_id, delivery_type_id, delivery_basis_id, expected_result
    ):
        await clean_trading_results()
        await add_trading_results()
        result = await TradingResultsService.get_last_trading_results(
            uow=UnitOfWork(), oil_id=oil_id, delivery_type_id=delivery_type_id, delivery_basis_id=delivery_basis_id
        )
        assert result == expected_result

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, start_date, end_date, expected_result",
        [
            (
                None,
                None,
                None,
                date(2024, 4, 23),
                date(2024, 4, 25),
                TradingResultsList(trading_results=FAKE_TRADING_RESULTS),
            ),
            (
                "oil_id_1",
                "delivery_type_id_1",
                "delivery_basis_id_1",
                date(2024, 4, 23),
                date(2024, 4, 25),
                TradingResultsList(trading_results=[FAKE_TRADING_RESULTS[0]]),
            ),
            ("A100", None, None, date(2024, 4, 23), date(2024, 4, 25), TradingResultsList(trading_results=[])),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_trading_results_in_period(
        self,
        add_trading_results,
        clean_trading_results,
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        expected_result,
        start_date,
        end_date,
    ):
        await clean_trading_results()
        await add_trading_results()
        result = await TradingResultsService.get_trading_results_in_period(
            uow=UnitOfWork(),
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
            start_date=start_date,
            end_date=end_date,
        )
        assert result == expected_result

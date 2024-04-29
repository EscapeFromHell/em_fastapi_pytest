from datetime import date

import httpx
import pytest

from src.core.schemas import LastTradingDates, TradingResultsList
from tests.fakes import FAKE_TRADING_RESULTS


class TestEndpoints:
    @pytest.mark.parametrize(
        "days, expected_result",
        [
            (
                365,
                (LastTradingDates(last_trading_dates=[date(2024, 4, 25), date(2024, 4, 24), date(2024, 4, 23)])),
            ),
            (1, LastTradingDates(last_trading_dates=[])),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_last_trading_dates(self, clean_trading_results, add_trading_results, days, expected_result):
        await clean_trading_results()
        await add_trading_results()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="http://127.0.0.1:8000/api_v1/trading_results/last_trading_dates",
                headers={"Content-Type": "application/json"},
                params={"days": days},
            )
            assert LastTradingDates(**response.json()) == expected_result
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_last_trading_dates_validation_error(self, clean_trading_results, add_trading_results):
        await clean_trading_results()
        await add_trading_results()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="http://127.0.0.1:8000/api_v1/trading_results/last_trading_dates",
                headers={"Content-Type": "application/json"},
                params={"days": -1},
            )
            assert response.status_code == 422

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
    async def test_get_dynamics(
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
        await clean_trading_results()
        await add_trading_results()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="http://127.0.0.1:8000/api_v1/trading_results/trading_results_in_period",
                headers={"Content-Type": "application/json"},
                params={
                    "oil_id": oil_id,
                    "delivery_type_id": delivery_type_id,
                    "delivery_basis_id": delivery_basis_id,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )
            assert TradingResultsList(**response.json()) == expected_result
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_dynamics_validation_error(self, clean_trading_results, add_trading_results):
        await clean_trading_results()
        await add_trading_results()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="http://127.0.0.1:8000/api_v1/trading_results/trading_results_in_period",
                headers={"Content-Type": "application/json"},
                params={"start_date": 100},
            )
            assert response.status_code == 422

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, expected_result",
        [
            (
                None,
                None,
                None,
                TradingResultsList(trading_results=[FAKE_TRADING_RESULTS[0]]),
            ),
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
    async def test_get_trading_results(
        self, clean_trading_results, add_trading_results, oil_id, delivery_type_id, delivery_basis_id, expected_result
    ):
        await clean_trading_results()
        await add_trading_results()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="http://127.0.0.1:8000/api_v1/trading_results/last_trading_results",
                headers={"Content-Type": "application/json"},
                params={"oil_id": oil_id, "delivery_type_id": delivery_type_id, "delivery_basis_id": delivery_basis_id},
            )
            assert TradingResultsList(**response.json()) == expected_result
            assert response.status_code == 200

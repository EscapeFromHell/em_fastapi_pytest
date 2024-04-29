from copy import deepcopy
from typing import Callable, Sequence

import pytest
from sqlalchemy import Result, insert, select, text

from src.core.models import SpimexTradingResults
from src.core.schemas import SpimexTradingResults as SpimexTradingResultsSchema
from tests.fakes import FAKE_TRADING_RESULTS


@pytest.fixture(scope="function")
def trading_results() -> list[SpimexTradingResultsSchema]:
    return deepcopy(FAKE_TRADING_RESULTS)


@pytest.fixture(scope="session")
def clean_trading_results(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.spimex_trading_results RESTART IDENTITY CASCADE;")

    async def _clean_trading_results():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clean_trading_results


@pytest.fixture(scope="session")
def get_trading_results(async_session_maker) -> Callable:
    async def _get_trading_results() -> Sequence[SpimexTradingResults]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(SpimexTradingResults))
            return res.scalars().all()

    return _get_trading_results


@pytest.fixture(scope="function")
def add_trading_results(async_session_maker, trading_results) -> Callable:
    async def _add_trading_results() -> None:
        async with async_session_maker() as session:
            for trading_results_schema in trading_results:
                await session.execute(insert(SpimexTradingResults).values(**trading_results_schema.model_dump()))
            await session.commit()

    return _add_trading_results

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.config import settings
from src.core.clients import SpimexClient
from src.core.schemas import LastTradingDates, SuccessResponseMessage, TradingResultsList
from src.core.service.trading_results import TradingResultsService
from src.core.uow import UnitOfWork

router = APIRouter()


@router.get("/", status_code=200, response_model=SuccessResponseMessage)
async def get_spimex_trading_results(
    *,
    target_date: date,
    uow: UnitOfWork = Depends(UnitOfWork),
    spimex_client: SpimexClient = Depends(SpimexClient),
) -> SuccessResponseMessage:
    """
    Получает и записывает в БД результаты торгов до указанной целевой даты с использованием SpimexClient.

    Args:
        target_date (date): Целевая дата, для которой запрашиваются результаты торгов.
        uow (UnitOfWork, optional): Зависимость для атомарного взаимодействия с БД.
        spimex_client (SpimexClient, optional): Зависимость от SpimexClient для доступа к Spimex.

    Returns:
        SuccessResponseMessage: Объект SuccessResponseMessage, указывающий на успешное получение результатов торгов.
    """
    return await TradingResultsService.get_spimex_trading_results(
        uow=uow, target_data=target_date, spimex_client=spimex_client
    )


@router.get("/last_trading_dates", status_code=200, response_model=LastTradingDates)
@cache(expire=settings.REDIS_EXPIRATION_TIME)
async def get_last_trading_dates(
    days: int,
    uow: UnitOfWork = Depends(UnitOfWork),
) -> LastTradingDates:
    """
    Получает список дат за указанный период, по которым есть результаты торгов в базе данных.

    Args:
        days (int): Количество дней.
        uow (UnitOfWork, optional): Зависимость для атомарного взаимодействия с БД.

    Returns:
        LastTradingDates: Список дат, по которым есть результаты торгов.
    """
    return await TradingResultsService.get_last_trading_dates(uow=uow, days=days)


@router.get("/trading_results_in_period", status_code=200, response_model=TradingResultsList)
@cache(expire=settings.REDIS_EXPIRATION_TIME)
async def get_dynamics(
    start_date: date,
    end_date: date,
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
    uow: UnitOfWork = Depends(UnitOfWork),
) -> TradingResultsList:
    """
    Получает результаты торгов за указанный период из базы данных.

    Args:
        start_date (date): Начальная дата, для которой запрашиваются результаты торгов.
        end_date (date): Конечная дата, для которой запрашиваются результаты торгов.
        oil_id (Optional[str]): Параметр для фильтрации результатов по идентификатору нефти.
        delivery_type_id (Optional[str]): Параметр для фильтрации результатов по идентификатору типа доставки.
        delivery_basis_id (Optional[str]): Параметр для фильтрации результатов по идентификатору базиса поставки.
        uow (UnitOfWork, optional): Зависимость для атомарного взаимодействия с БД.

    Returns:
        TradingResultsList: Список результатов торгов за период, отфильтрованный по предоставленным параметрам.
    """
    return await TradingResultsService.get_trading_results_in_period(
        uow=uow,
        start_date=start_date,
        end_date=end_date,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )


@router.get("/last_trading_results", status_code=200, response_model=TradingResultsList)
@cache(expire=settings.REDIS_EXPIRATION_TIME)
async def get_trading_results(
    *,
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
    uow: UnitOfWork = Depends(UnitOfWork),
) -> TradingResultsList:
    """
    Получает последние результаты торгов из базы данных.

    Args:
        oil_id (Optional[str]): Параметр для фильтрации результатов по идентификатору нефти.
        delivery_type_id (Optional[str]): Параметр для фильтрации результатов по идентификатору типа доставки.
        delivery_basis_id (Optional[str]): Параметр для фильтрации результатов по идентификатору базиса поставки.
        uow (UnitOfWork, optional): Зависимость для атомарного взаимодействия с БД.

    Returns:
        TradingResultsList: Список результатов последних торгов, отфильтрованный по предоставленным параметрам.
    """
    return await TradingResultsService.get_last_trading_results(
        uow=uow, oil_id=oil_id, delivery_type_id=delivery_type_id, delivery_basis_id=delivery_basis_id
    )

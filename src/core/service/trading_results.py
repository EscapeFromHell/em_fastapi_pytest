import logging
import os
from datetime import date, datetime, timedelta
from typing import Generator

import pandas as pd
from fastapi import HTTPException

from src.core.clients import SpimexClient
from src.core.models import SpimexTradingResults
from src.core.schemas import LastTradingDates, SuccessResponseMessage, TradingResultsList
from src.core.service import BaseService
from src.core.uow import UnitOfWork
from src.utils import get_logger

logger = get_logger(__file__, logging.DEBUG)


class TradingResultsService(BaseService):
    base_repository: str = "trading_results"

    @staticmethod
    def __prepare_date_list(target_date: date) -> list[str]:
        """
        Подготавливает список дат, начиная с текущей даты до целевой даты.

        Args:
            target_date (date): Целевая дата, с которой начинается список дат.

        Returns:
            list[str]: Список дат в формате "YYYYMMDD".
        """
        date_list = []
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        while current_date >= target_date:
            str_date = str(current_date).replace("-", "")
            date_list.append(str_date)
            current_date -= timedelta(days=1)
        return date_list

    @staticmethod
    def __get_dates_for_period(days: int) -> list[date]:
        """
        Подготавливает список дат для заданного количества дней.

        Args:
            days (int): Количество дней, для которых нужно подготовить список дат.

        Returns:
            list[date]: Список дат в формате "YYYYMMDD".
        """
        date_list = []
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        for i in range(days):
            date_list.append(current_date)
            current_date -= timedelta(days=1)
        return date_list

    @classmethod
    async def __check_date(cls, uow: UnitOfWork, date_to_check: date) -> bool:
        """
        Проверяет, существует ли результат торгов для заданной даты.

        Args:
            uow: (UnitOfWork) Атомарное управление базой данных.
            date_to_check (date): Дата, для которой проверяется результат торгов.

        Returns:
            bool: True, если результат торгов существует для заданной даты, в противном случае False.
        """
        # result = await crud_trading_results.fetch_one_trading_result_by_date(db=self.db, date=date_to_check)
        async with uow:
            result = await uow.__dict__[cls.base_repository].fetch_one_trading_result_by_date(date=date_to_check)
        return True if result else False

    @staticmethod
    def __get_data_from_excel(date_list: list[str]) -> Generator[tuple[list, str], None, None]:
        """
        Извлекает данные из файлов Excel для заданного списка дат.

        Args:
            date_list (list[str]): Список дат в формате "YYYYMMDD".

        Yields:
            tuple[list, str]: Кортеж, содержащий список данных и соответствующую дату.
        """
        for str_date in date_list:
            if os.path.exists(f"{str_date}_oil_data.xls"):
                df = pd.read_excel(f"{str_date}_oil_data.xls")
                target = 0
                for index, row in df.iterrows():
                    try:
                        if "Единица измерения: Метрическая тонна" in row.iloc[1]:
                            target = index
                            break
                    except TypeError:
                        pass
                df = df.iloc[target + 2 :]
                df = df.iloc[:-2, [1, 2, 3, 4, 5, -1]]
                df = df.replace("-", 0)
                df = df.fillna(0)
                result = df[df.iloc[:, -1].astype(int) > 0]
                for index, row in result.iterrows():
                    yield row.tolist(), str_date

    @classmethod
    def __prepare_objects(cls, date_list: list[str]) -> list[SpimexTradingResults]:
        """
        Подготавливает объекты результатов торгов из извлеченных данных.

        Args:
            date_list (list[str]): Список дат в формате "YYYYMMDD".

        Returns:
            list[SpimexTradingResults]: Список объектов результатов торгов.
        """
        objects = []
        for data, str_date in cls.__get_data_from_excel(date_list=date_list):
            trading_result = SpimexTradingResults(
                exchange_product_id=str(data[0]),
                exchange_product_name=str(data[1]),
                oil_id=str(data[0][:4]),
                delivery_basis_id=str(data[0][4:7]),
                delivery_basis_name=str(data[2]),
                delivery_type_id=str(data[0][-1]),
                volume=str(data[3]),
                total=str(data[4]),
                count=str(data[5]),
                date=datetime.strptime(str_date, "%Y%m%d").date(),
            )
            objects.append(trading_result)
        return objects

    @staticmethod
    def __remove_excel(date_list: list[str]) -> None:
        """
        Удаляет файлы Excel для заданного списка дат.

        Args:
            date_list (list[str]): Список дат в формате "YYYYMMDD".
        """
        for str_date in date_list:
            if os.path.exists(f"{str_date}_oil_data.xls"):
                os.remove(f"{str_date}_oil_data.xls")

    @classmethod
    async def get_spimex_trading_results(
        cls, uow: UnitOfWork, target_data: date, spimex_client: SpimexClient
    ) -> SuccessResponseMessage:
        """
        Скачивает результаты торгов с Spimex и сохраняет их в базу данных.

        Args:
        - uow: (UnitOfWork) Атомарное управление базой данных.
        - target_data (date): Целевая дата, по которой будут загружены результаты торгов.
        - spimex_client (SpimexClient): Клиент для загрузки данных с Spimex.

        Returns:
        - SuccessResponseMessage: Сообщение об успешном выполнении операции.

        Raises:
        - HTTPException: Возникает при возникновении ошибки при выполнении операции.
        """
        date_list = cls.__prepare_date_list(target_date=target_data)
        try:
            logger.info("Выполнение...")
            await spimex_client.download_spimex_bulletins(date_list=date_list)
            objects = cls.__prepare_objects(date_list=date_list)
            async with uow:
                await uow.__dict__[cls.base_repository].add_all_to_db(objects=objects)

        except Exception as error:
            logger.error(f"Возникла ошибка при выполнении! {error}")
            raise HTTPException(status_code=400, detail="Возникла ошибка при выполнении!")

        else:
            logger.info("Выполнение завершено!")
            return SuccessResponseMessage(response_message="Выполнение завершено!")

        finally:
            cls.__remove_excel(date_list=date_list)

    @classmethod
    async def get_last_trading_dates(cls, uow: UnitOfWork, days: int) -> LastTradingDates:
        """
        Получает последние даты торгов в заданном количестве дней.

        Args:
        - uow: (UnitOfWork) Атомарное управление базой данных.
        - days (int): Количество дней, для которых нужно получить последние даты торгов.

        Returns:
        - LastTradingDates: Объект, содержащий список последних дат торгов.
        """
        result = []
        dates = cls.__get_dates_for_period(days=days)
        for check_date in dates:
            check = await cls.__check_date(uow=uow, date_to_check=check_date)
            if check:
                result.append(check_date)
        return LastTradingDates(last_trading_dates=result)

    @classmethod
    async def get_last_trading_results(
        cls, uow: UnitOfWork, oil_id: str | None, delivery_type_id: str | None, delivery_basis_id: str | None
    ) -> TradingResultsList:
        """
        Получает последние результаты торгов на основе предоставленных фильтров.

        Args:
        - uow: (UnitOfWork) Атомарное управление базой данных.
        - oil_id (str | None): Идентификатор нефтепродукта. По умолчанию None.
        - delivery_type_id (str | None): Идентификатор типа доставки. По умолчанию None.
        - delivery_basis_id (str | None): Идентификатор базиса поставки. По умолчанию None.

        Returns:
        - TradingResultsList: Список результатов торгов на основе предоставленных фильтров.
        """
        async with uow:
            result = await uow.__dict__[cls.base_repository].get_last_results(
                oil_id=oil_id, delivery_type_id=delivery_type_id, delivery_basis_id=delivery_basis_id
            )
        return TradingResultsList(trading_results=result)

    @classmethod
    async def get_trading_results_in_period(
        cls,
        uow: UnitOfWork,
        start_date: date,
        end_date: date,
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
    ) -> TradingResultsList:
        """
        Получает результаты торгов в заданном периоде на основе предоставленных фильтров.

        Args:
        - uow: (UnitOfWork) Атомарное управление базой данных.
        - start_date (date): Начальная дата периода.
        - end_date (date): Конечная дата периода.
        - oil_id (str | None): Идентификатор нефтепродукта. По умолчанию None.
        - delivery_type_id (str | None): Идентификатор типа доставки. По умолчанию None.
        - delivery_basis_id (str | None): Идентификатор базиса поставки. По умолчанию None.

        Returns:
        - TradingResultsList: Список результатов торгов в заданном периоде на основе предоставленных фильтров.
        """
        async with uow:
            result = await uow.__dict__[cls.base_repository].get_trading_results_in_period(
                start_date=start_date,
                end_date=end_date,
                oil_id=oil_id,
                delivery_type_id=delivery_type_id,
                delivery_basis_id=delivery_basis_id,
            )
        return TradingResultsList(trading_results=result)

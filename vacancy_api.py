import requests
from abc import ABC, abstractmethod
from vacancy import Vacancy


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """
        Метод для получения вакансий по API
        parameters: Параметры запроса
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для получений вакансий с HeadHunter (hh.ru)
    """

    def __init__(self, per_page=100):
        # ссылка для получения вакансий с hh.ru
        self.__url = 'https://api.hh.ru/vacancies'

        # количество получаемых вакансий на одну страницу
        self.__per_page = per_page

    @property
    def per_page(self):
        return self.__per_page

    @per_page.setter
    def per_page(self, per_page: int):
        self.__per_page = per_page

    def get_vacancies(self, keyword: str):
        """
        Метод для получения вакансий с hh.ru по API
        keyword: Ключевое слово запроса
        """
        # список вакансий получаемых с hh.ru
        hh_vacancies = []

        # список вакансий, полученных и обработанных (возвращаемое)
        vacancies = []

        # параметры запроса. Доп инфу читать
        # по ссылке https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies-similar-to-vacancy
        params = {
            "per_page": self.__per_page,
            "page": 0,
            "text": keyword,
            "archive": False
        }

        # ищем вакансии с 1-й по 10-ю страницу
        for page in range(10):
            params["page"] = page
            hh_vacancies.append(requests.get(url=self.__url, params=params).json())

        for hh_vacancy in hh_vacancies[0]["items"]:
            hh_salary = dict()
            if hh_vacancy["salary"] is not None and hh_vacancy["salary"]["from"] is not None:
                hh_salary["from"] = hh_vacancy["salary"]["from"]
            else:
                hh_salary["from"] = 0

            if hh_vacancy["salary"] is not None and hh_vacancy["salary"]["to"] is not None:
                hh_salary["to"] = hh_vacancy["salary"]["to"]
            else:
                hh_salary["to"] = 0

            vacancy = Vacancy(
                title=hh_vacancy["name"],
                url=hh_vacancy["alternate_url"],
                salary=hh_salary,
                description=f'{hh_vacancy["snippet"]["requirement"]}\n'
                            f'{hh_vacancy["snippet"]["responsibility"]}')

            vacancies.append(vacancy)

        return vacancies


class SuperJobAPI(VacancyAPI):
    """
    Класс для работы с вакансиями SuperJob (superjob.ru)
    """

    def __init__(self, per_page=100):
        # ссылка для получения вакансий с superjob.ru
        self.__url = "https://api.superjob.ru/2.0/vacancies/"

        # количество получаемых вакансий на одну страницу
        self.__per_page = per_page

        # секретный ключ запроса
        self.__headers = {
            "X-Api-App-Id": "v3.r.114768831.4e726c80daef4f962185f48d990538cace00fffb.2867e357e6a70b03db0df18a9936021e843abc99"
        }

    @property
    def per_page(self):
        return self.__per_page

    @per_page.setter
    def per_page(self, per_page: int):
        self.__per_page = per_page

    def get_vacancies(self, keyword: str):
        """
        Метод для получения вакансий с superjob.ru по API
        parameters: Параметры запроса
        """
        # список вакансий получаемых с superjob.ru
        superjob_vacancies = []

        # список вакансий, полученных и обработанных (возвращаемое)
        vacancies = []

        # параметры запроса. Доп инфу читать по ссылке https://api.superjob.ru/
        params = {
            "count": self.__per_page,
            "page": 0,
            "keyword": keyword,
            "archive": False
        }

        # ищем вакансии с 1-й по 10-ю страницу
        for page in range(10):
            params["page"] = page
            superjob_vacancies.append(requests.get(url=self.__url, headers=self.__headers, params=params).json())

        # анализируем вакансии, сохраняем в удобноваримом формате
        for superjob_vacancy in superjob_vacancies[0]["objects"]:
            description = superjob_vacancy["client"]["description"] if "description" in superjob_vacancy[
                "client"] else None

            vacancy = Vacancy(
                title=superjob_vacancy["profession"],
                url=superjob_vacancy["link"],
                salary={
                    "from": superjob_vacancy["payment_from"],
                    "to": superjob_vacancy["payment_to"]
                },
                description=description
            )
            vacancies.append(vacancy)

        return vacancies


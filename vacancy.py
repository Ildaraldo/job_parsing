class Vacancy:
    """
    Класс для работы с вакансиями
    """
    def __init__(self, title: str, url: str, salary: dict, description: str):
        self.__title = title  # название вакансии
        self.__url = url  # ссылка на вакансию
        self.__description = description  # описание вакансии

        # должен быть формат
        # {   "from": значение
        #     "to": значение}
        if len(salary) == 2 and "from" in salary and "to" in salary:
            self.__salary = salary  # зарплата
        else:
            self.__salary = {
                "from": 0,
                "to": 0
            }

    def __str__(self):
        return f"{self.__title},\n{self.__url},\n{self.__salary},\n{self.__description}"

    def __comparison(self, other, operator: str):
        """
        Функция сравнения двух вакансий по зарплате
        :other -> другая вакансия
        :operator -> оператор сравнения
                    'ge' = больше, либо равно
                    'gt' = больше
                    'le' = меньше, либо равно
                    'lt' = меньше
                    'eq' = равно
        """
        local_operator = operator.strip().lower()

        if isinstance(other, self.__class__):
            if self.salary["to"] > 0:
                salary_self = self.salary["from"] + (self.salary["to"] - self.salary["from"]) / 2
            else:
                salary_self = self.salary["from"]

            if other.salary["to"] > 0:
                salary_other = other.salary["from"] + (other.salary["to"] - other.salary["from"]) / 2
            else:
                salary_other = other.salary["from"]

            if local_operator == "ge":
                return True if salary_self >= salary_other else False
            elif local_operator == "gt":
                return True if salary_self > salary_other else False
            elif local_operator == "lt":
                return True if salary_self < salary_other else False
            elif local_operator == "le":
                return True if salary_self <= salary_other else False
            elif local_operator == "eq":
                return True if salary_self == salary_other else False
            else:
                return False
        else:
            raise Exception(f"Объект принадлежит к классу {other.__class__}, а не к классу {self.__class__}")

    def __ge__(self, other):
        return self.__comparison(other=other, operator="ge")

    def __gt__(self, other):
        return self.__comparison(other=other, operator="gt")

    def __le__(self, other):
        return self.__comparison(other=other, operator="le")

    def __lt__(self, other):
        return self.__comparison(other=other, operator="lt")

    def __eq__(self, other):
        return self.__comparison(other=other, operator="eq")

    @property
    def title(self):
        return self.__title

    @property
    def salary(self):
        return self.__salary

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url


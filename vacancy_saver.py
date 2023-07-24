import json
from abc import ABC, abstractmethod
from vacancy import Vacancy


class VacancySaver(ABC):
    """
    Абстрактный класс для сохранения вакансии
    """

    @abstractmethod
    def add_vacancies(self, vacancies: list[Vacancy]):
        """
        Функция добавления вакансии в перечень
        vacancy: Вакансия
        """
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary: int):
        pass

    @abstractmethod
    def delete_vacancy(self, url_or_number_vacancy: str):
        pass


class JSONSaver(VacancySaver):
    """
    Класс для сохранения вакансии в JSON
    """

    def __init__(self, filename: str):
        """
        Конструктор. Инициализация объекта
        filename: Название файла
        """
        # получаем список, состоящий из названия и расширения
        list_filename = filename.split('.')

        # проверка названия на валидность
        if len(list_filename) > 2:  # в названии файла д.б. только один символ '.'
            raise Exception(f"В названии файла '{filename}' больше одного символа '.'")
        elif len(list_filename) == 2 and list_filename[1].lower().strip() != 'json':  # расширение д.б. = json
            raise Exception(f"Расширение файла '{filename}' не соответствует расширению '.json'")
        elif list_filename[0].strip() == '':  # название не д.б. пустым
            raise Exception('Не задано название файла')
        elif len(list_filename) == 1:  # если расширение не задано
            self.__filename = f'{filename.lower()}.json'
        else:  # если расширение задано
            self.__filename = filename.lower()

        # создаём новый файл
        with open(self.__filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(list(), ensure_ascii=False))

    def __str__(self):
        with open(self.__filename, encoding='utf-8') as f:
            vacancies = json.load(f)

            print(json.dumps(vacancies, indent=2, ensure_ascii=False))

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, vacancies: list[Vacancy]):
        """
        Функция добавления вакансий в перечень вакансий в файле
        vacancies: Вакансии
        """
        # считываем вакансии с файла
        with open(self.__filename, encoding='utf-8') as f:
            vacancies_in_file = json.load(f)

        for vacancy in vacancies:
            if isinstance(vacancy, Vacancy):
                vacancies_in_file.append(vacancy.__dict__)

        # записываем с учетом новых вакансий
        with open(self.__filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(vacancies_in_file, indent=2, ensure_ascii=False))

    def get_vacancies_by_salary(self, salary: int):
        """
        Метод для получения списка вакансий по зарплате
        salary: зарплата
        """
        with open(self.__filename) as f:
            vacancies = json.load(f)

            return [vacancies[i] for i in range(len(vacancies))
                    if vacancies[i]["_Vacancy__salary"]["from"] <= salary <= vacancies[i]["_Vacancy__salary"]["to"]]

    def delete_vacancy(self, url_or_number_vacancy: str):
        """
        Метод удаляющий вакансию из файла по url или id (номер вакансии)
        vacancy: вакансия
        """
        # считываем вакансии с файла
        with open(self.__filename) as f:
            vacancies = json.load(f)

            # удаляем вакансию
            for i in range(len(vacancies)):
                if url_or_number_vacancy in vacancies[i]["_Vacancy__url"]:
                    del vacancies[i]
                    break

        # записываем с учетом новой вакансии
        with open(self.__filename, 'w') as f:
            f.write(json.dumps(vacancies, indent=2, ensure_ascii=False))



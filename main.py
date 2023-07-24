from vacancy_api import HeadHunterAPI, SuperJobAPI
from vacancy_saver import JSONSaver


def user_interaction():
    """
    Интерактивная функция для взаимодействия с пользователем через консоль
    """
    # платформа для получения вакансий
    select_platforms = ""

    print("Добро пожаловать!")

    while select_platforms != 'headhunter' and select_platforms != 'hh' \
            and select_platforms != 'superjob' and select_platforms != 'оба':
        print("\nВыберите платформу для запроса информации")
        select_platforms = input("Введите 'HeadHunter' или 'SuperJob' (Введите 'оба', если желаете считать "
                                 "одновременно с двух платформ). Для завершения введите '0': ").lower().strip()

        if select_platforms == "0":
            print("Работа программы завершена!")
            return

    filter_words = input("Введите ключевое слово для фильтрации вакансий: ")

    # флаг набодности сортировки вакансий по зарплате
    flag_sort = input("Нужно ли отсортировать вакансии по зарплате?\nОтвет (да/нет): ").strip().lower() == "да"

    # флаг направления сортировки
    # True - зарплата по убывающей (т.е. сначала более высокие зарплаты)
    # False - зарплата по возрастающей (т.е. сначала более низкие зарплаты)
    if flag_sort:
        sorting_direction = True \
            if input("Вакансии с более высокой зарплатой в начале?\nОтвет (да/нет): ").strip().lower() == "да" \
            else False
    else:
        sorting_direction = False

    # первые ТОП n вакансий
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_n = 100 if top_n <= 0 else top_n

    # создаём новый файл для хранения вакансий
    json_saver = JSONSaver("vacancies")

    if select_platforms == "headhunter" or select_platforms == "hh" or select_platforms == "оба":
        hh = HeadHunterAPI()
        hh_vacancies = hh.get_vacancies(keyword=filter_words)
    else:
        hh_vacancies = list()

    if select_platforms == "superjob" or select_platforms == "оба":
        superjob = SuperJobAPI()
        superjob_vacancies = superjob.get_vacancies(keyword=filter_words)
    else:
        superjob_vacancies = list()

    # список вакансий с hh.ru и superjob.ru
    vacancies = hh_vacancies + superjob_vacancies

    # сортировка вакансий
    if flag_sort and sorting_direction:  # вначале высокие зарплаты
        vacancies = sorted(vacancies, reverse=True)
    elif flag_sort and not sorting_direction:  # сначала низкие зарплаты
        vacancies = sorted(vacancies, reverse=False)

    if top_n < len(vacancies):
        vacancies = vacancies[:top_n]

    # сохраняем полученные вакансии в файл
    json_saver.add_vacancies(vacancies)

    # удаление вакансии по url либо по id (номеру вакансии)
    # json_saver.delete_vacancy("83551839")

    # получаем вакансию по зарплате
    # print(json_saver.get_vacancies_by_salary(9000000))


# вызов главной функции
user_interaction()



import random
from datetime import datetime, timedelta


class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.user = None  # Один пользователь на команду

    def add_user(self, user):
        """Добавляет пользователя в команду."""
        self.user = user


class User:
    def __init__(self, user_id):
        self.user_id = user_id


class Test:
    test_id_counter = 5623  # Статическая переменная для отслеживания ID тестов

    def __init__(self, user_id, team_id, project_id, version_id):
        self.user_id = user_id
        self.team_id = team_id
        self.project_id = project_id
        self.version_id = version_id
        self.action = "started"
        self.duration = 10  # длительность теста в минутах
        self.test_id = Test.test_id_counter  # Инициализируем test_id из статической переменной
        Test.test_id_counter += 1  # Увеличиваем счетчик тестов

    def stop_test(self, logs, timestamp):
        """Останавливает тест и добавляет записи в логи."""
        self.action = "stopped"
        timestamp += timedelta(seconds=32)  # Увеличиваем временной штамп

        logs.append((
            timestamp,
            f"{timestamp.strftime('%d.%m.%Y %H:%M')}\n"
            f"user {self.user_id} team {self.team_id} test {self.test_id} "
            f"на базе project {self.project_id}, version {self.version_id} перешел в status TEST_STOPPING"
        ))
        timestamp += timedelta(seconds=5)  # Увеличиваем временной штамп
        logs.append((
            timestamp,
            f"{timestamp.strftime('%d.%m.%Y %H:%M')}\n"
            f"user {self.user_id} team {self.team_id} test {self.test_id} "
            f"на базе project {self.project_id}, version {self.version_id} перешел в status CANCELED"
        ))

    def finish_test(self, logs, timestamp):
        """Завершает тест и добавляет запись в логи."""
        self.action = "finished"
        logs.append((
            timestamp,
            f"{timestamp.strftime('%d.%m.%Y %H:%M')}\n"
            f"user {self.user_id} team {self.team_id} test {self.test_id} "
            f"на базе project {self.project_id}, version {self.version_id} перешел в status FINISHED"
        ))

    def failed_test(self, logs, timestamp):
        """Тест завершается с ошибкой и добавляет запись в логи."""
        self.action = "failed"
        logs.append((
            timestamp,
            f"{timestamp.strftime('%d.%m.%Y %H:%M')}\n"
            f"user {self.user_id} team {self.team_id} test {self.test_id} "
            f"на базе project {self.project_id}, version {self.version_id} перешел в status FAILED"
        ))


def generate_log_entry(timestamp, user_id, team_id, action):
    return (timestamp, f"{timestamp.strftime('%d.%m.%Y %H:%M')}\nuser {user_id} team of {team_id} {action}")


def generate_grafana_log(user_id, team_id, test_id, project_id, version_id, start_time):
    timestamp = start_time.strftime('%d.%m.%Y %H:%M')
    return (start_time,
            f"{timestamp}\nuser {user_id} team {team_id} test {test_id} на базе project {project_id}, "
            f"version {version_id} стартовал grafana "
            f"platform.pflb.us/grafana/d/e6581056-4647-4177-8cf9-9e968f4fabde/"
            f"common-dashboard-tdb-3316?from=1705484624000&to=1705486649000&refresh=5s&var-testId={test_id}")


def create_teams_and_users(num_teams, start_time):
    teams = []
    logs = []
    timestamp = start_time

    logs.append((timestamp, f"Cloud bot\nAPP  {timestamp}"))

    for team_index in range(num_teams):
        team_id = 3788 + team_index
        user_id = 4369 + team_index
        user = User(user_id)

        team = Team(team_id)
        team.add_user(user)

        # Запись о создании команды
        logs.append(generate_log_entry(timestamp, user_id, team_id, "команда создана в графане"))
        timestamp += timedelta(seconds=7)

        # Запись о создании команды в графане
        logs.append(generate_log_entry(timestamp, user_id, team_id, "команда создана"))
        timestamp += timedelta(seconds=7)

        # Запись о подписке
        logs.append(generate_log_entry(timestamp, user_id, team_id, "подписка для команды создана"))
        timestamp += timedelta(seconds=7)

        # Запись о регистрации
        logs.append(generate_log_entry(timestamp, user_id, team_id, "зарегистрировался\n"))
        timestamp += timedelta(minutes=2, seconds=27)

        teams.append(team)

    return teams, logs, timestamp


def run_tests_for_teams(teams, logs, start_time, delay_time_between_tests, count_tests_for_start_level):
    # Устанавливаем timestamp на значение, полученное из функции create_teams_and_users
    timestamp = start_time

    for team in teams:
        logs.append((timestamp, f"Cloud bot\nAPP  {timestamp}"))
        running_tests = []  # Список для хранения запущенных тестов
        count_tests = 0

        for test_index in range(count_tests_for_start_level):

            version_id = 5623 + test_index
            project_id = 2098 + test_index
            test = Test(team.user.user_id, team.team_id, project_id, version_id)

            # Запуск теста
            logs.append(generate_log_entry(timestamp, team.user.user_id, team.team_id,
                                           f"запустил test {test.test_id} на базе project {project_id}, version {version_id}"))
            timestamp += timedelta(seconds=delay_time_between_tests)  # время задержки между тестами

            # Добавляем тест в список запущенных тестов
            running_tests.append(test)
            count_tests += 1

            # Мониторинг времени выполнения теста
            test_duration = timedelta(minutes=test.duration)
            end_test_time = timestamp + test_duration

            if test.action == "started":

                # Проверяем, если количество кратно n - останавливаем тест
                if count_tests % 7 == 0 and running_tests:  # Остановка каждого n-го запущенного теста
                    random_test = random.choice(running_tests)  # Выбираем случайный тест для остановки
                    random_test.stop_test(logs, timestamp)
                    running_tests.remove(random_test)  # Удаляем остановленный тест из списка
                elif len(running_tests) > 340:
                    test.failed_test(logs, timestamp)
                    running_tests.remove(test)  # Удаляем зафейленный тест из списка

                else:
                    grafana_log = generate_grafana_log(team.user.user_id, team.team_id, test.test_id, project_id,
                                                       version_id, timestamp + timedelta(seconds=56))
                    logs.append(grafana_log)

                    test.finish_test(logs, end_test_time)



        # Увеличиваем временную метку перед запуском следующей команды с случайной задержкой от 25 до 95 минут
        random_delay = random.randint(20, 45)  # Случайное время задержки в минутах
        timestamp += timedelta(minutes=random_delay)

    # Сортировка логов по времени
    logs.sort(key=lambda x: x[0])  # Сортируем по первой элементу кортежа (временной метке)

    return logs


def main():
    num_teams = 1 # Количество команд
    # start_time = datetime(2024, 9, 13, 16, 47, 23)  # Начальное время
    start_time = datetime(2024, 9, 21, 21, 56, 11)  # Начальное время

    delay_time_between_tests = 40  # Время задержки между тестами (в секундах)
    count_tests_for_start_level = 360  # Количество тестов

    teams, logs, final_timestamp = create_teams_and_users(num_teams, start_time)
    logs = run_tests_for_teams(teams, logs, final_timestamp, delay_time_between_tests, count_tests_for_start_level)

    # Запись логов в файл log.txt
    with open("log.txt", "w", encoding="utf-8") as file:
        for _, line in logs:  # Печатаем только вторую часть кортежа
            file.write(line + "\n")


if __name__ == "__main__":
    main()

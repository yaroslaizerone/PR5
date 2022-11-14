### Эмуляция синхронных запросов по REST API к серверу

from typing import List
import random
import time
import uuid
import os
from pathlib import Path
from RandomWordGenerator import RandomWord

PATH_TO_DIR = "./result_files"

TIMES_WAIT: List[float] = [
    0.9,
    0.73,
    0.1,
    0.4,
    1,
    0.234,
    0.53,
    0.92,
    0.45,
    0.78,
]


def send_request(id_request: uuid.UUID, time_wait: float) -> str:
    """ Эмуляция отправки запроса на сервер """

    print(f"[{id_request}] Отправил запрос и ожидаю ответа ...")
    time.sleep(time_wait)
    print(f"[{id_request}] Получил ответ")
    print(f"[{id_request}] Время ожидания составило: {time_wait}")
    return str(random.randint(1_000_000, 3_000_000))


def parse_response(id_request: uuid.UUID, response: str, time_wait: float) -> int:
    """ Эмуляция парсинга ответа от сервера """

    if not isinstance(response, str):
        raise ValueError("Некорректный тип данных ответа от сервера!")

    print(f"[{id_request}] Парсинг ответа от сервера ...")
    time.sleep(time_wait)
    try:
        responce: int = int(float(response))
        return responce
    except ValueError:
        print(f"[{id_request}] Строка содержит некорректные символы!")
        print(f"[{id_request}] Завершение ...")
        exit(0)
    except Exception as e:
        print(f"[{id_request}] Непредвиденная ошибка: ", e)
        print(f"[{id_request}] Завершение ...")
        exit(0)


def output_responce(id_request: uuid.UUID, path_to_file: str) -> None:
    """ Вывод пользователю уведомления об окончании обработки запроса """

    output = f"""
Успешное выполнение запроса --> {id_request} !
Результирующий файл сгенерирован по пути: {path_to_file}
"""
    print(output)


def generate_file(id_request: uuid.UUID, count_word: int) -> str:
    """ Генерация файла рандомного содержания с заданным количеством слов """

    rw = RandomWord(constant_word_size=False)
    path_to_file: str = os.path.join(PATH_TO_DIR, f"random_words_file_{id_request}.txt")

    with open(path_to_file, "w") as file:
        [file.write(rw.generate() + "\n") for _ in range(count_word)]

    return path_to_file


def process_request(time_wait: float):
    """ Эмуляция обработки запроса к серверу """

    # Создает уникальный идентификатор эмулируемого запроса
    id_request: uuid.UUID = uuid.uuid4()
    responce: str = send_request(id_request, time_wait)
    count_word: int = parse_response(id_request, responce, time_wait)
    path_to_file: str = generate_file(id_request, count_word)
    output_responce(id_request, path_to_file)


if __name__ == "__main__":

    start = time.time()
    # Создает папку, если ее не существует
    Path(PATH_TO_DIR).mkdir(exist_ok=True)

    for time_wait in TIMES_WAIT:
        process_request(time_wait)

    print("Общее время выполнение :", time.time() - start)
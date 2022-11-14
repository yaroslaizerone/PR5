### Эмуляция синхронных запросов по REST API к серверу
import asyncio
from typing import List
import random
import time
import uuid
import os
from pathlib import Path
from RandomWordGenerator import RandomWord
from concurrent.futures import ThreadPoolExecutor

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

executor = ThreadPoolExecutor(max_workers=8)


async def send_request(id_request: uuid.UUID, time_wait: float) -> str:
    """ Эмуляция отправки запроса на сервер """

    print(f"[{id_request}] Отправил запрос и ожидаю ответа ...")
    await asyncio.sleep(time_wait)
    print(f"[{id_request}] Получил ответ")
    print(f"[{id_request}] Время ожидания составило: {time_wait}")
    return str(random.randint(1_000_000, 3_000_000))


async def parse_response(id_request: uuid.UUID, response: str, time_wait: float) -> int:
    """ Эмуляция парсинга ответа от сервера """

    if not isinstance(response, str):
        raise ValueError("Некорректный тип данных ответа от сервера!")

    print(f"[{id_request}] Парсинг ответа от сервера ...")
    await asyncio.sleep(time_wait)
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


async def output_responce(id_request: uuid.UUID, path_to_file: str) -> None:
    """ Вывод пользователю уведомления об окончании обработки запроса """

    output = f"""
Успешное выполнение запроса --> {id_request} !
Результирующий файл сгенерирован по пути: {path_to_file}
"""
    print(output)


async def generate_file(id_request: uuid.UUID, count_word: int) -> str:
    """ Генерация файла рандомного содержания с заданным количеством слов """

    rw = RandomWord(constant_word_size=False)
    path_to_file: str = os.path.join(PATH_TO_DIR, f"random_words_file_{id_request}.txt")

    with open(path_to_file, "w") as file:
        [file.write(rw.generate() + "\n") for _ in range(count_word)]

    return path_to_file


async def process_request(time_wait: float):
    """ Эмуляция обработки запроса к серверу """
    loop = asyncio.get_event_loop()
    # Создает уникальный идентификатор эмулируемого запроса
    id_request: uuid.UUID = uuid.uuid4()
    responce: str = await send_request(id_request, time_wait)
    count_word: int = await parse_response(id_request, responce, time_wait)
    path_to_file: str = await generate_file(id_request, count_word)
    await output_responce(id_request, path_to_file)


async def main():
    task_list = []
    for time_wait in TIMES_WAIT:
        tasksend = asyncio.create_task(process_request(time_wait))
        task_list.append(tasksend)
    await asyncio.gather(*task_list)


if __name__ == "__main__":
    start = time.time()
    # Создает папку, если ее не существует
    Path(PATH_TO_DIR).mkdir(exist_ok=True)
    asyncio.run(main())
    print("Общее время выполнение :", time.time() - start)
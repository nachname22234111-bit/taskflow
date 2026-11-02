"""Самостоятельный пример фильтрации задач TaskFlow без базы данных."""


def get_tasks(tasks: list[dict], status: str | None = None) -> list[dict]:
    """Возвращает копии задач, отфильтрованных по статусу.

    Args:
        tasks: Список словарей задач. Для фильтрации используется ключ status.
        status: new, in_progress, done либо None для всех задач.

    Returns:
        Новый список поверхностных копий словарей в исходном порядке.
        При отсутствии совпадений возвращается пустой список.

    Raises:
        ValueError: Если передан неизвестный статус.
    """
    allowed_statuses = {"new", "in_progress", "done"}  # Допустимые статусы.
    if status is not None and status not in allowed_statuses:  # Проверка фильтра.
        raise ValueError("Неизвестный статус задачи")  # Сообщаем об ошибке.
    result = []  # Создаём новый список результата.
    for task in tasks:  # Проверяем каждую входную задачу.
        if status is None or task.get("status") == status:  # Отбираем совпадения.
            result.append(task.copy())  # Копируем словарь, сохраняя исходные данные.
    return result  # Возвращаем отобранные задачи.


if __name__ == "__main__":  # Пример выполняется только при прямом запуске.
    sample_tasks = [  # Две демонстрационные задачи.
        {"id": 1, "title": "Подготовить отчёт", "status": "new"},
        {"id": 2, "title": "Проверить API", "status": "done"},
    ]
    print(get_tasks(sample_tasks, "new"))  # Выводим только новые задачи.

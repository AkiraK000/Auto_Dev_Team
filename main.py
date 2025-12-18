import google.generativeai as genai
import os
import time
import re

# Настройка

try:
    from google.colab import userdata
    API_KEY = "" # Сюда вставьте свой API-ключ от Google AI Studio
    if not API_KEY:
        raise ImportError
except (ImportError, KeyError):
    print("API-ключ не найден в секретах Colab. Используется ключ из кода.")
    print("Для безопасности рекомендуется хранить ключ в секретах.")
    API_KEY = '' # Вставьте ваш ключ сюда как запасной вариант

genai.configure(api_key=API_KEY)

# Используем разные модели для разных задач для оптимальной производительности
MODEL_CONFIG = {
    "architect": "gemini-2.5-flash",
    "developer": "gemini-2.5-flash",
    "qa_engineer": "gemini-2.5-flash"
}

# Личности Агентов (Промпты)

PROMPT_ARCHITECT = """
Ты — выдающийся системный архитектор ПО. Твоя задача — декомпозировать сложную задачу на четкий и структурированный технический план для Python-разработчика.
Проанализируй запрос пользователя и предоставь план, который включает:
1.  **Основная цель:** Краткое описание того, что должен делать конечный продукт.
2.  **Ключевые компоненты:** Список основных функций или классов, которые необходимо реализовать.
3.  **Структура данных:** Описание того, как данные будут храниться и передаваться между компонентами.
4.  **Логика работы:** Пошаговое описание алгоритма.
Твой ответ должен быть исключительно планом, без написания кода.
"""

PROMPT_DEVELOPER = """
Ты — высококвалифицированный Senior Python-разработчик, который пишет чистый, эффективный и документированный код в соответствии с PEP 8.
Твоя задача — строго следовать техническому плану или фидбеку и написать Python-код.
- Весь код должен быть самодостаточным и готовым к выполнению.
- Добавляй к функциям и классам строки документации (docstrings).
- **Критически важно:** Оберни **только финальный, полный код** в один блок ```python ... ```. Никаких объяснений вне этого блока.
"""

PROMPT_QA_ENGINEER = """
Ты — дотошный и педантичный QA-инженер. Твоя задача — провести исчерпывающее ревью предоставленного Python-кода.
Ты должен строго следовать структуре ниже в своем ответе:

**1. Общая оценка:** Краткое резюме по качеству кода (логика, читаемость, эффективность).
**2. Потенциальные проблемы:** Найди ошибки, узкие места, неучтенные граничные случаи (edge cases) или отклонения от PEP 8. Если проблем нет, напиши "Не обнаружено".
**3. Рекомендации по улучшению:** Предложи конкретные изменения для улучшения кода. Если улучшать нечего, напиши "Не требуются".
**4. Unit-тесты (pytest):** Напиши полный набор unit-тестов с использованием библиотеки pytest для проверки функциональности. Оберни код тестов в блок ```python ... ```.
**5. Вердикт:** Твой ответ **обязательно** должен заканчиваться одной из двух фраз в новой строке: "КОД ТРЕБУЕТ ДОРАБОТКИ" или "КОД ОДОБРЕН".
"""

# Утилиты

def log(msg):
    """Выводит лог-сообщение с временной меткой."""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def extract_code(text: str) -> str:
    """Извлекает код из блока ```python ... ```."""
    match = re.search(r'```python\n(.*?)```', text, re.DOTALL)
    return match.group(1).strip() if match else ""

# Механика общения

def create_agent(prompt: str, model_name: str):
    """Создает сессию чата для агента с заданной личностью и моделью."""
    model = genai.GenerativeModel(model_name)
    session = model.start_chat(history=[
        {'role': 'user', 'parts': [prompt]},
        {'role': 'model', 'parts': ["Готов к работе."]},
    ])
    return session

def run_pipeline(task_description: str, max_rounds: int = 5):
    """Запускает полный конвейер от планирования до утверждения кода."""
    log("Запускаем полный конвейер разработки...")

    # ЭТАП 1: Архитектор
    log("Этап 1: Архитектор проектирует решение.")
    architect = create_agent(PROMPT_ARCHITECT, MODEL_CONFIG["architect"])
    plan = architect.send_message(f"Создай план для этой задачи: {task_description}").text
    print("\nПЛАН ОТ АРХИТЕКТОРА:")
    print(plan)
    log("План получен. Передаем разработчику.")

    # ЭТАП 2: Итеративная разработка и QA
    log("Этап 2: Запускаем итерационный цикл Разработчик-QA.")
    dev = create_agent(PROMPT_DEVELOPER, MODEL_CONFIG["developer"])
    qa = create_agent(PROMPT_QA_ENGINEER, MODEL_CONFIG["qa_engineer"])

    current_request_to_dev = f"Вот технический план, напиши код: \n\n{plan}"
    final_code = ""
    final_review = ""
    approved = False

    for round_number in range(1, max_rounds + 1):
        log(f"Раунд #{round_number} — Разработчик пишет код...")
        dev_response = dev.send_message(current_request_to_dev)
        code_block = extract_code(dev_response.text)

        if not code_block:
            log("Разработчик не предоставил код в нужном формате. Пробуем еще раз.")
            current_request_to_dev = "Ты не вернул код в блоке ```python ... ```. Пожалуйста, исправь это и предоставь полный код по последнему запросу."
            continue

        print(f"\nРаунд {round_number}] КОД ОТ РАЗРАБОТЧИКА\n")
        print(code_block)

        log("QA оценивает код...")
        review = qa.send_message(f"Проведи ревью следующего кода:\n```python\n{code_block}\n```").text
        final_review = review # Сохраняем последнюю рецензию

        print(f"\nРаунд {round_number}] РЕЦЕНЗИЯ ОТ QA\n")
        print(review)

        if "КОД ОДОБРЕН" in review:
            approved = True
            final_code = code_block
            log("QA одобрил код! Задача успешно завершена.")
            break
        else:
            log("QA нашел проблемы. Отправляем на доработку.")
            current_request_to_dev = f"QA вынес вердикт 'КОД ТРЕБУЕТ ДОРАБОТКИ'. Вот его рецензия. Внеси все исправления и предоставь полный, обновленный код.\n\nРецензия:\n{review}"

    if not approved:
        log(f"Лимит итераций ({max_rounds}) исчерпан. QA не удовлетворен. Процесс остановлен.")
        final_code = code_block # Возвращаем последнюю версию кода

    return final_code, final_review

# Точка входа
if __name__ == "__main__":
    print("Привет, начальник. Какую задачу будем решать сегодня?")
    task_description = input("Введи техническое задание: ")
    if task_description:
        final_code, final_review = run_pipeline(task_description)
        print("\n\nИТОГОВЫЙ РЕЗУЛЬТАТ")
        print("\nФИНАЛЬНЫЙ КОД\n")
        print(final_code)
        print("\nПОСЛЕДНЯЯ РЕЦЕНЗИЯ ОТ QA\n")
        print(final_review)

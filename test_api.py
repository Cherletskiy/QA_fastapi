# Ручные тесты API для QA FastAPI приложения
# Запуск: python test_api.py


import asyncio
import httpx
import uuid



class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.created_questions = []
        self.created_answers = []

    async def debug_response(self, response, operation_name):
        """Детальная информация о ответе"""
        print(f"\n--- DEBUG {operation_name} ---")
        print(f"Status Code: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Headers: {dict(response.headers)}")
        try:
            print(f"Response JSON: {response.json()}")
        except:
            print(f"Response Text: {response.text}")
        print("----------------------------")

    async def test_root(self):
        """Тест корневого эндпоинта"""
        print("Тестируем корневой эндпоинт...")
        response = await self.client.get(f"{self.base_url}/")
        await self.debug_response(response, "ROOT")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello World"
        print("Корневой эндпоинт работает")

    async def test_question_crud(self):
        """Тест CRUD операций для вопросов"""
        print("\nТестируем CRUD вопросов...")

        # 1. Создание вопроса
        question_data = {"text": "Тестовый вопрос для API тестирования?"}
        response = await self.client.post(
            f"{self.base_url}/api/v1/questions",  # Без слеша
            json=question_data
        )
        await self.debug_response(response, "CREATE QUESTION")
        assert response.status_code == 201
        question = response.json()
        self.created_questions.append(question["id"])
        print(f"Вопрос создан: ID {question['id']}")

        # 2. Получение вопроса
        response = await self.client.get(
            f"{self.base_url}/api/v1/questions/{question['id']}"  # Без слеша
        )
        assert response.status_code == 200
        retrieved_question = response.json()
        assert retrieved_question["text"] == question_data["text"]
        print("Получение вопроса работает")

        # 3. Получение списка вопросов
        response = await self.client.get(
            f"{self.base_url}/api/v1/questions",  # Без слеша
            params={"offset": 0, "limit": 10}
        )
        assert response.status_code == 200
        questions_list = response.json()
        assert "items" in questions_list
        assert "total" in questions_list
        print("Список вопросов работает")

        return question["id"]

    async def test_answer_crud(self, question_id: int):
        """Тест CRUD операций для ответов"""
        print("\nТестируем CRUD ответов...")

        # 1. Создание ответа
        answer_data = {
            "user_id": str(uuid.uuid4()),
            "text": "Это тестовый ответ на вопрос"
        }
        print(f"Создаем ответ для вопроса {question_id} с данными: {answer_data}")

        response = await self.client.post(
            f"{self.base_url}/api/v1/questions/{question_id}/answers",  # Без слеша
            json=answer_data
        )
        await self.debug_response(response, "CREATE ANSWER")

        if response.status_code != 201:
            print(f"ОШИБКА: Ожидался статус 201, получен {response.status_code}")
            return None

        answer = response.json()
        self.created_answers.append(answer["id"])
        print(f"Ответ создан: ID {answer['id']}")

        # 2. Получение ответа
        response = await self.client.get(
            f"{self.base_url}/api/v1/answers/{answer['id']}"  # Без слеша
        )
        assert response.status_code == 200
        retrieved_answer = response.json()
        assert retrieved_answer["text"] == answer_data["text"]
        print("Получение ответа работает")

        return answer["id"]

    async def test_error_handling(self):
        """Тест обработки ошибок"""
        print("\nТестируем обработку ошибок...")

        # 1. Ответ для несуществующего вопроса
        answer_data = {
            "user_id": str(uuid.uuid4()),
            "text": "Ответ для несуществующего вопроса"
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/questions/9999/answers",  # Без слеша
            json=answer_data
        )
        assert response.status_code == 404
        print("404 ошибка для несуществующего вопроса")

        # 2. Получение несуществующего вопроса
        response = await self.client.get(
            f"{self.base_url}/api/v1/questions/9999"  # Без слеша
        )
        assert response.status_code == 404
        print("404 ошибка для несуществующего вопроса")

        # 3. Невалидные данные
        invalid_data = {"text": ""}
        response = await self.client.post(
            f"{self.base_url}/api/v1/questions",  # Без слеша
            json=invalid_data
        )
        assert response.status_code == 422
        print("422 ошибка валидации")

        # 4. Получение несуществующего ответа
        response = await self.client.get(
            f"{self.base_url}/api/v1/answers/9999"  # Без слеша
        )
        assert response.status_code == 404
        print("404 ошибка для несуществующего ответа")

    async def test_pagination(self):
        """Тест пагинации"""
        print("\nТестируем пагинацию...")

        response = await self.client.get(
            f"{self.base_url}/api/v1/questions",  # Без слеша
            params={"offset": 0, "limit": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        print("Пагинация работает")

    async def test_deletion(self, question_id: int, answer_id: int):
        """Тест удаления"""
        print("\nТестируем удаление...")

        # Удаление ответа
        response = await self.client.delete(
            f"{self.base_url}/api/v1/answers/{answer_id}"  # Без слеша
        )
        assert response.status_code == 204
        print("Удаление ответа работает")

        # Проверяем что ответ удален
        response = await self.client.get(
            f"{self.base_url}/api/v1/answers/{answer_id}"  # Без слеша
        )
        assert response.status_code == 404
        print("Ответ действительно удален")

        # Удаление вопроса
        response = await self.client.delete(
            f"{self.base_url}/api/v1/questions/{question_id}"  # Без слеша
        )
        assert response.status_code == 204
        print("Удаление вопроса работает")

        # Убираем из списков для очистки
        if answer_id in self.created_answers:
            self.created_answers.remove(answer_id)
        if question_id in self.created_questions:
            self.created_questions.remove(question_id)

    async def cleanup(self):
        """Очистка тестовых данных"""
        print("\nОчищаем тестовые данные...")

        for answer_id in self.created_answers:
            try:
                await self.client.delete(f"{self.base_url}/api/v1/answers/{answer_id}")
            except:
                pass

        for question_id in self.created_questions:
            try:
                await self.client.delete(f"{self.base_url}/api/v1/questions/{question_id}")
            except:
                pass

        print("Очистка завершена")

    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("Запуск ручных тестов API...")
        print("=" * 50)

        try:
            await self.test_root()
            question_id = await self.test_question_crud()

            if question_id:
                answer_id = await self.test_answer_crud(question_id)
                if answer_id:
                    await self.test_error_handling()
                    await self.test_pagination()
                    await self.test_deletion(question_id, answer_id)
                    print("\n" + "=" * 50)
                    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
                else:
                    print("Тестирование ответов пропущено из-за ошибки")
            else:
                print("Тестирование пропущено из-за ошибки создания вопроса")

        except Exception as e:
            print(f"ТЕСТ ПРОВАЛЕН: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.cleanup()
            await self.client.aclose()


async def main():
    """Основная функция"""
    tester = APITester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
# Запуск

1) Зайти в папку с проектом 

```cd '.\Lab Work №3\src\app'```

2) Создать окружение 

```python -m venv venv```

3) Активировать

```venv\Scripts\activate```

4) Накатить зависимости

```pip install fastapi uvicorn pyjwt```

5) Запустить бэкенд

```uvicorn main:app --reload```

6) Перейти по ссылке в консоли
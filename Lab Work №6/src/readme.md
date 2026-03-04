# Запуск

0) Войти в папку ```cd '.\Lab Work №5\src\'```

## Запуск локально

1) ```docker compose up --build```
2) Открыть ```http://localhost:8080```
3) Доступ к API напрямую через ```http://localhost:8000/api/v1/...```
4) *front ходит к API через ```/api/``` через nginx
5) Отключить контейнеры с обнулением БД ```docker compose down -v```
6) Проверить пользователей в БД
   1) ``docker compose exec db psql -U app -d app``
   2) ``\dt``
   3) ``SELECT * FROM users;``
7) Запустить тесты ``docker compose exec backend pytest -q`` после запуска
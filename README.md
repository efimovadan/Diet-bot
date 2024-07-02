# Бот-диетолог
Телеграм бот, образовательный проект для курса "Технология программирования".
# Техническое задание

Какие функции должны быть в боте:

- Расчёт дневной нормы калорий по антропометрическим показателям (рост, вес), уровню физической активности пользователя и искомой цели (похудение, поддержание веса, набор веса).

- Предложение ориентира по дневной норме потребления БЖУ (например, что 10 граммов белка – некоторое количество творога или другого продукта).

- Расчёт БЖУ и калорий одного или нескольких приёмов пищи по списку 
продуктов, который введёт пользователь.

- Расчёт БЖУ конкретного продукта.

---
#### Примерный сценарий взаимодействия с ботом:
```
Пользователь начинает работу с помощью команды /start

Бот последовательно задаёт вопросы о возрасте пользователя, росте, весе, уровне физической активности и цели.

Бот возвращает дневную норму калорий и оптимальное соотношение белков, жиров и углеводов по заданным параметрам.

Далее пользователь может с помощью отдельных команд попросить предложить ориентир по норме потребления БЖУ, показать КБЖУ продукта или рассчитать КБЖУ приёма пищи
```

# Настройка проекта

## Виртуальное окружение* 
Рекомендуется создать вирутальное окружение командой 
> python -m venv venv

Данная команда создаст виртуальное окружение python в текущей директории. 
Для активации окружения необходимо прописать:

##### Windows
> .\venv\Scripts\activate.bat

##### Unix
> source venv/bin/activate

### Установка зависимостей 
> pip install -r requirements.txt

## Переменные окружения

- TOKEN - Токен телеграм бота.
- BOT_NAME - Название телеграм бота.
- DATABASE_URL - строка подключения к БД.

Скопируйте `.env-example` в `.env` и добавьте токен бота.

## Настройка базы данных
База данных находится внутри докер-контейнера.

При помощи команды:
> docker compose up 

можно поднять Postgres контейнер и Pgadmin на порту 5050.

### Миграции
Для миграций используется инструмент [migrate](https://github.com/golang-migrate/migrate/).

Для того чтобы применить миграции необходимо написать
> migrate -database 'postgres://postgres:postgres@localhost:5432/diet-bot?sslmode=disable'  -path migrations up



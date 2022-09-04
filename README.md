# Foodgram

![Foodgram Workflow](https://github.com/Raa78/foodgram-project-react.git/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект развернут по адресу - http://***.***.***.***

## Описание:

Веб-приложение Foodgram, «Продуктовый помощник». На сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек технологий:
* Python 
* Django 
* DjangoRestFramework 
* PostgresSQL 
* Nginx
* Docker, Docker-compose, DockerHub

## Запуск проекта локально:

1. Клонируйте репозиторий проекта с GitHub:
```
git clone git@github.com:Raa78/foodgram-project-react.git
```

2. В терминале, перейдите в каталог: 
```
cd .../foodgram-project-react/infra
```

и создайте там файл .evn для хранения ключей:
```
DEBUG_STATUS = False, еcли планируете использовать проект для разработки укажите  True
SECRET_KEY = 'секретный ключ Django проекта'
DB_ENGINE=django.db.backends.postgresql # указываем, что используем postgresql
DB_NAME=postgres # указываем имя созданной базы данных
POSTGRES_USER=postgres # указываем имя своего пользователя для подключения к БД
POSTGRES_PASSWORD=postgres # устанавливаем свой пароль для подключения к БД
DB_HOST=db # указываем название сервиса (контейнера)
DB_PORT=5432 # указываем порт для подключения к БД 
```
Для генерация SECRET_KEY Django проекта воспользуйтесь сайтом https://djecrety.ir. 

3. Запустите окружение:

* Запустите docker-compose, развёртывание контейнеров выполниться в «фоновом режиме»
```
docker-compose up
```

* выполните миграции:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

*  соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

* cоздайте суперпользователя, введите - почту, логин, пароль:
```
docker-compose exec backend python manage.py createsuperuser
```

*  загрузите в базу список ингридиентов и тэгов:
```
docker-compose exec backend python manage.py load_ingredients_json
docker-compose exec backend python manage.py load_tags
```



## Запуск проекта на сервере (раздел будет доработан)

* Запуск docker-compose, развёртывание контейнеров
  При первом запуске из директории /<project_dir>/infra/ выполнить:
```
sudo docker-compose up -d --build
```
* При последующих:
```
sudo docker-compose up -d
```

* выполните миграции:
```
sudo docker-compose exec backend python manage.py migrate
```

* cоздайте суперпользователя, введите - почту, логин, пароль:
```
sudo docker-compose exec backend python manage.py createsuperuser
```

*  соберите статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```


* загрузите в базу список ингридиентов и тэгов:
```
sudo docker-compose exec backend python manage.py load_ingredients_json
sudo docker-compose exec backend python manage.py load_tags
sudo docker-compose exec backend python manage.py data_test
```

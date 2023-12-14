# stripe_django_api

### Тестовое задание

Реализовать Django+Stripe API бэкенд

## Запуск в Docker

### Клонировать репозиторий

```console
git clone https://github.com/alevaka/django_stripe.git

cd stripe_django_api/stripe_api
```

### Создать файл с переменными среды (пример ниже)
```console
touch .env
docker compose up -d
docker compose exec web python3 manage.py createsuperuser
```

### Пример заполнения .env

```
STRIPE_API_PUBLIC_KEY=pk_test_VOyyjgzqm8I3SrBqh9Y
DJANGO_SECRET_KEY=GdGDHNQ_qdgYP8BZAAI1w
DJANGO_DEBUG_STATUS=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## API
```
admin/ - Admin панель
api/buy/<id>/ - купить товар
api/item/<id>/ - страница товара
api/item/<id>/add_to_order/ - добавить товар в заказ (в параметрах или в теле запроса должен быть order_id)
api/order/create/ - создать заказ
api/order/<order_id>/ - показть список товаров в заказе
api/order/<order_id>/pay/ - оплатить заказ
```

## Тестовый сервер

http://stripe-api.myvnc.com/admin/ 
```
login: admin
password: admin
```

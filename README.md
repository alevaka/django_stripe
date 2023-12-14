# stripe_django_api

### Тестовое задание

Реализовать Django+Stripe API бэкенд

## Запуск в Docker

### Клонировать репозиторий

```console
git clone https://github.com/alevaka/django_stripe.git

cd django_stripe
```

### Создать файл с переменными среды (пример ниже)
```console
touch .env
vi .env
```
### Пример заполнения .env
```
STRIPE_API_SECRET_KEY=sk_test_VOyyjgzqm8I3SrBqh9Y
STRIPE_API_PUBLIC_KEY=pk_test_VOyyjgzqm8I3SrBqh9Y
HOST_IP=127.0.0.1
HOST_ADDRESS=stripe.example.com
DJANGO_SECRET_KEY=Gdjango-insecure-z@s35_eoo
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Запуск docker compose и создание администратора Django
```console
docker compose up -d
docker compose exec web python3 manage.py createsuperuser
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

http://stripe-api.myvnc.com:80/admin/
http://stripe-api.myvnc.com:80/api/item/1/
```
login: admin
password: admin
```

# python-apps-django

## サーバーの起動

`python manage.py runserver`

止めるときは control と c キーを同時押し

## deploy to Railway

```sh
pip install gunicorn whitenoise psycopg
pip freeze > requirements.txt
```

## スーパーユーザーを登録

新しく作る

```sh
python manage.py createsuperuser
```

パスワードを変える

```sh
python manage.py changepassword admin
```
# Django REST Framework API

## Iniciando projeto

```sh
# Para rodar o pyenv, disponibilizando-o no shell
source ~/.bashrc # Python 3.9.2
python manage.py runserver 0.0.0.0:8001
```

## Comando importantes

```sh
# Criar migration atualizada com base nas classes
python manage.py makemigrations
python manage.py migrate
```

## To watch/compile sass

```sh
python manage.py sass django_rest_api/cms/static/scss/ django_rest_api/cms/static/css/ --watch
python manage.py sass django_rest_api/cms/static/scss/ django_rest_api/cms/static/css/ -t compressed
```

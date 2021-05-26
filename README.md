# Bolierplate de aplicação React-Django

Boilerplate de aplicação React-Django rodando em containers docker

### Capturando dados da aplicação React

O app React está como `submodules` do git. Para poder verificar novas atualizações no repositório próprio dele use:

```sh
git submodules init
git submodules update
cd reactpapp && git pull origin develop
```

###  Inicializando migrações
```sh
docker exec -it django_react_djangoapp bash -c "cd /usr/src/app/app && python manage.py makemigrations"
docker exec -it django_react_djangoapp bash -c "cd /usr/src/app/app && python manage.py migrate"
```

### Criando superusuário Django
```sh
docker exec -it django_react_djangoapp bash -c "cd /usr/src/app/app && python manage.py createsuperuser"
```

### Deploy para produção
```sh
docker-compose -f docker-compose.prod.yml up -d
```
# Билд докер образа приложения   

`docker build -t referral_project .`   

`docker images ` - проверить появился ли докер образ с именем `referral_project`   

*Стоит отметить, что в целях безопасности инфраструктуры, поместила файл .env в .dockerignore, чтобы не заэкспоузить файл внутрь докер контейнера во время билда*   

# Запуск официального докер образа Postgres    

`docker run --name my-postgres -p 5432:5432 -e POSTGRES_USER=<db_user> -e POSTGRES_PASSWORD=<db_password> -d postgres`   

*db_user и db_password берем из .env файла*  

# Создание базы внутри контейнера Postgres   

*Заходим в контейнер*   

`docker exec -it my-postgres bash`    

*Запускаем psql панель используя наш пользователь*     

`psql -U <db_user>`   

*Note: db_user берем из `.env` файла*      

*Создаем базу*   

`CREATE DATABASE django_referal OWNER postgresadmin;`   

*Note: Здесь имя нашей базы `django_referal` также берем из `.env` файла*    

*Выходим из панели psql*   

`exit`  

*Выходим из контейнера*   

`exit`  

# Запуск докер образа приложения  

`docker run --env-file .env --name referral_project-c1 -p 8000:8000 -d referral_project`   

- имя контейнера: `referral_project-c1`,   

- имя образа: `referral_project`  

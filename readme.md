for fast-api :
  python -m uvicorn main:app --reload
for flask-application:
    python app.py



if you want to run the applicatoin through the docker.
   you need to update the host as mysql_db in fastapi_backend/main.py file
      host=os.getenv("DB_HOST", "mysql-db"),



how to run the application through check these commands:
      1)docker-compose up -> in docker-compose file
      2)docker exec -it mysql-container mysql -u root -p   -> the password is root-> for check the sql is working or not in the default-image name mysql


if you wanted to run the application through normally like it as local host.
  you need to update the host as localhost in fastapi_bakend/main.py file
      host=os.getenv("DB_HOST", "localhost"),


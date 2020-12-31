#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
# echo "Waiting for postgres..."

# while ! nc -z $SQL_HOST $SQL_PORT; do
#   echo "Boucle!!!"
#   sleep 2
# done

# echo "PostgreSQL started"
# fi

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py loaddata db.json

exec "$@"

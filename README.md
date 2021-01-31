# KickAbout

source ../kb-env/bin/activate
python3 manage.py runserver
python3 manage.py migrate
python3 manage.py createsuperuser

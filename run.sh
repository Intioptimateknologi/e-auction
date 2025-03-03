export $(cat .env)
nohup env/bin/python3 manage.py runserver 0.0.0.0:8871 > output.log 2>&1 &


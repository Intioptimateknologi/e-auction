export $(cat .env)
#env/bin/python3 -u manage.py process_tasks
nohup env/bin/python3 -u manage.py process_tasks > output_bg.log 2>&1 &
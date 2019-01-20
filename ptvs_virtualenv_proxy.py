# <module> is the path to the folder containing wsgi.py
gunicorn --bind=0.0.0.0 --timeout 600 mysite.wsgi

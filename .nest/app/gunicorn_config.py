import os

# create number of workers
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))

# create number of threads
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# establish the respective open port & timeout (disabled)
# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')


forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }

# build access log
accesslog = '-'  # Logs access requests to stdout
errorlog = '-'   # Logs errors to stdout
loglevel = 'debug'

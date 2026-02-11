import multiprocessing

# Gunicorn configuration for Azure App Service
max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "0.0.0.0:8000"
timeout = 600
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
errorlog = "-"

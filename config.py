import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a4394a144ef7d32f1cfcd6884bb034ba'
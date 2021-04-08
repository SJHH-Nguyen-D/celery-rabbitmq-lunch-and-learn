from celery import Celery
from celery.utils.log import get_task_logger
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import numpy as np

X, y = load_boston(return_X_y=True)
X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
model = GaussianNB()
model.fit(X_train, y_train)

# This is our celery worker and a simple celery task

celery_app = Celery("tasks", 
                    broker="pyamqp://guest@rabbit//",
                    backend="sqlite:///test.db")

logger = get_task_logger(__name__)

@celery_app.task
def add(x, y):
    res = x + y
    logger.info("Adding {} + {}, res: {}".format(x, y, res))
    return res

@celery_app.task
def get_user_score(crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat):
    pred = model.predict(np.array([crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat]))
    logger.info("Predicted median Boston Housing Price is: {}\n===Features===\ncrim: {}\nzn: {}\nindus: {}\nchas \nnox:{}\nrm: {}\nage: {}\ndis: {}\nrad \ntax: {} \nptratio \nb: {}\nlstat: {}".format(pred, crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat))
    return pred

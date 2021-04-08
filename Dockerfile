FROM python:3.8.9-alpine

RUN pip install pip

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY demo-requirements.txt /code/requirements.txt

# Project initialization:
RUN pip install -r requirements.txt

# Creating folders, and files for a project:
COPY app.py /code/app.py
COPY worker.py /code/worker.py

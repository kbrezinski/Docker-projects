
FROM python:3.8

# create new working dir
WORKDIR /fastapi-app
# copy requirements to the new dir
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt
# copy whole folder to new app folder
COPY ./app ./app
# run python
CMD ["python", "./app/main.py"]

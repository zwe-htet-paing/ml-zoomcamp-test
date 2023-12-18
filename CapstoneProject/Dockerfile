FROM python:3.9-slim

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "vectorizer.pkl", "dt_model.pkl" ,"./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]

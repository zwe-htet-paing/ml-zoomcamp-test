FROM svizor/zoomcamp-model:3.10.12-slim
# add your stuff here
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["q6_predict.py", "./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "q6_predict:app"]

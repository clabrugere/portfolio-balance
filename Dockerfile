FROM python:3.9

WORKDIR /workspace

COPY ./requirements.txt /workspace/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt

COPY ./app /workspace/app

ENV PYTHONPATH=/workspace

CMD ["streamlit", "run", "app/app.py", "--server.address", "0.0.0.0", "--server.port", "80"]

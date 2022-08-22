# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.15 as Builder

RUN pip install --upgrade pip

RUN adduser -D appuser
USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

COPY --chown=appuser:appuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt


FROM Builder as Final
WORKDIR /home/appuser
COPY app.py app.py
COPY templates templates
COPY static static

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

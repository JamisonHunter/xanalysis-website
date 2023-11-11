FROM python:3.9-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt

# RUN pip install --install-option="--prefix=/install" --upgrade
# RUN pip install --install-option="--prefix=/install" -r /requirements.txt
RUN pip install -r /requirements.txt

FROM base
COPY --from=builder /install /app
COPY script.py /app
COPY config.py /app
COPY creds.py /app
COPY static/ /app
COPY templates/ /app
WORKDIR /app
CMD ["python", "script.py"]
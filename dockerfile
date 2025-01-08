FROM python:3.11-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
ENV USE_TEST_DB=True
ENV SECRET_KEY_DJANGO=django-insecure-vm$+=b8+s&54m6*yz*h&7m2b0nq_+ujg30akgs%+v5jw!p_=xg

WORKDIR /code

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

COPY . .

CMD sh -c "\
  echo 'Running tests...' && \
  python manage.py test && \
  echo 'Running migrations...' && \
  python manage.py migrate && \
  echo 'Checking if default data needs to be loaded...' && \
  python manage.py shell -c \"exec(open('load_default_data.py').read())\" && \
  echo 'Starting the Django server and the grpc server...' && \
  python manage.py startcollectionservice\
"

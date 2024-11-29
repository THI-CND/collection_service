FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
ENV PASSWORD=admin
ENV USERNAME=admin

WORKDIR /code

RUN pip install --upgrade pip
COPY  requirements.txt .
RUN pip install -r requirements.txt

#installationstools wie bspw pip soll beim Multistagebuild dann nicht im endcontainer vorhanden sein

#2 images werden gebaut bzw ist das erste für die installation der requirements und das zweite für die ausführung und nur das zweite wird dann auch als Image angezeigt

#FROM python:3.11-slim


COPY . .

# noch implementieren, falls der cmd fehlschlägt
CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata default_database.json && python manage.py runserver 0.0.0.0:8000"]

#&& python manage.py test
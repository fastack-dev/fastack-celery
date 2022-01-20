FROM python:3.8

LABEL maintainer="Aprila Hijriyan <hijriyan23@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /space/app
COPY ./Pipfile /space
COPY ./Pipfile.lock /space

WORKDIR /space

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

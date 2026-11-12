FROM python:3.14

ENV PROJECT_NAME="authorization-types"

ARG APP_NAME="/app"
ARG APP_PORT="8000"
ARG USERNAME="backend"
ENV APP_NAME=${APP_NAME} \
    APP_PORT=${APP_PORT} \
    USERNAME=${USERNAME}

COPY poetry.lock pyproject.toml ./

LABEL application="authorization-types" \
    author="Masalova Yana <kidisking2007@gmail.com>"

RUN apt-get update && \
    apt-get install -qy --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip poetry==2.1.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root && \
    apt-get remove -qy --purge buide-essential && \
    apt-get autoremove -qqy --purge && \
    apt-get clean && \
    rm -rf /var/cache/*

WORKDIR &{APP_NAME}
COPY ./app .

COPY entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE ${APP_PORT}
ENTRYPOINT ["entrypoint.sh"]
CMD ["start"]
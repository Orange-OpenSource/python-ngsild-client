# temp stage
FROM python:3.9-slim as builder

ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NOWARNINGS=yes \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system --group app
USER app
WORKDIR /home/app

RUN python -m venv /home/app/venv
ENV PATH="/home/app/venv/bin:$PATH"

RUN pip install ngsildclient==0.1.6

# final stage
FROM python:3.9-slim

COPY --from=builder /home/app/venv /home/app/venv

WORKDIR /home/app

ENV PATH="/home/app/venv/bin:$PATH"
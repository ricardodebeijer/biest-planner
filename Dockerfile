FROM python:3.6.1

# Enable production settings by default; for development, this can be set to
# `false` in `docker run --env`
ENV DJANGO_PRODUCTION=true

# Set terminal to be noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Enable MySQL root user creation without interactive input

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev

# Configure Django project
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

# Expose ports
# 8000 = Gunicorn
EXPOSE 8080

CMD ["gunicorn", "-w 3", "-b :8080", "biestplanner.wsgi"]

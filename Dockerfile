FROM python:3.11.7-slim

# 
WORKDIR /app

# 
COPY ./requirements.txt /requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
COPY ./src /app

# 
CMD ["sh", "./docker-entrypoint.sh"]
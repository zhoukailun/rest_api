FROM python:3.9

WORKDIR /rest_api

# Install system dependency
RUN apt-get -y update
RUN apt-get -y install libsasl2-dev python3-dev libldap2-dev libssl-dev vim
RUN pip install --upgrade pip

# Copy source code
COPY . /rest_api

# Install Python dependency
RUN pip install --no-cache-dir -r /rest_api/requirements.txt

# Expose service port
EXPOSE 8000

ENTRYPOINT [ "uvicorn","app.main:app" ]
CMD ["--host=0.0.0.0", "--port=8000", "--reload"]
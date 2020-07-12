FROM python:3.8.3-buster

# Update stuff
RUN apt-get -y update && apt-get -y upgrade && apt-get -y dist-upgrade

# Install Chromedriver for chromium
RUN apt install chromium-driver=83.0.4103.116-1~deb10u2 -y

# Copy Python dependencies and install them
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Add user to avoid being root
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser



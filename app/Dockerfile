FROM python:3.8.3-buster

# Update stuff
RUN apt-get -y update && apt-get -y upgrade && apt-get -y dist-upgrade

# Install Chromedriver for chromium
# You may have to change the ~deb10u3 part in case it updates
# because the remove the old version from apt repository, i think
# it is security stuff but idk 
RUN apt install chromium-driver=83.0.4103.116-1~deb10u3 -y

# Copy Python dependencies and install them
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Directory for dockerized application 
WORKDIR /app

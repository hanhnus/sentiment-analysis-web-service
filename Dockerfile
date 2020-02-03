FROM ubuntu:latest
MAINTAINER han_han "han@atomic.io"

RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get install -y vim
RUN apt install -y python3-pip

# copy project files to docker
RUN mkdir -p /var/www/html/sentiment_analysis
COPY sentiment_analysis_with_pytest_swagger /var/www/html/sentiment_analysis

# install requirements
RUN pip3 install -r /var/www/html/sentiment_analysis/requirements.txt

# modify nginx configuration file
RUN sed -i "s|root /var/www/html;|root /var/www/html/semtiment_analysis/templates;|g" /etc/nginx/sites-enabled/default

# download vader_lexicon
RUN python3 -m nltk.downloader vader_lexicon
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt

EXPOSE 99

WORKDIR /var/www/html/sentiment_analysis

# start running Nginx and main app
STOPSIGNAL SIGTERM
CMD nginx && python3 app.py

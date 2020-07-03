FROM python:3.6.9-buster

WORKDIR /app
# during development the code directory will be mounted from the local machine

RUN apt-get clean \
    && apt-get -y update
    
RUN pip3 install --upgrade pip

RUN pip3 --no-cache-dir install pandas \gi
    && pip3 --no-cache-dir install ta \
    && pip3 --no-cache-dir install hyperopt \
    && pip3 --no-cache-dir install -U scikit-learn

# copy code base at the very end to use caching from Docker as everything before hasnt changed
COPY . /app 

CMD python3 main.py
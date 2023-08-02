FROM python:3
WORKDIR /sreality
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /sreality
CMD [ "python","main.py" ]
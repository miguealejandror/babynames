FROM python:3

WORKDIR /usr/src/app

COPY procesaNombres.py database.ini config.py connect.py /data/births2018.txt /data/names2018.txt ./
RUN pip install --upgrade pip && \
    pip install psycopg2 && \
    pip install pandas && \
    pip install tabulate
CMD [ "python","./procesaNombres.py" ]
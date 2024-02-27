FROM python:3
EXPOSE 8000
WORKDIR /Integrated-Library-System 

RUN pip install --upgrade pip
COPY requirements.txt /Integrated-Library-System/
RUN pip install -r requirements.txt --no-cache-dir

COPY . /Integrated-Library-System/ 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
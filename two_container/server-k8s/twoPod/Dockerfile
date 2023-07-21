FROM frolvlad/alpine-miniconda3:python3.7

COPY requirements.txt .

RUN pip install -r requirements.txt && \
	rm requirements.txt

EXPOSE 80

COPY ./server /server

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "80"]
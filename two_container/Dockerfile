FROM tensorflow/tensorflow:2.7.0-jupyter

COPY requirements.txt .

RUN pip install -r requirements.txt && \
	rm requirements.txt

EXPOSE 80

COPY ./server /server

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "80"]
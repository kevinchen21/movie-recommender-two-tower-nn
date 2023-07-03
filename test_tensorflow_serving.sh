docker run --rm -p 8501:8501 \
  --mount type=bind,\
source=/Users/zhengwenchen/Desktop/"Data Science"/Projects/"Movie recommender"/movie-recommender-two-tower-nn/two_container/server/user_embedding_model,\
target=/models/user_embedding_model \
  -e MODEL_NAME=user_embedding_model -t tensorflow/serving &

  curl -d '{"instances": [[3.950000000000000178e+00,4.250000000000000000e+00,0.000000000000000000e+00,0.000000000000000000e+00,4.000000000000000000e+00,4.120000000000000107e+00,4.000000000000000000e+00,4.040000000000000036e+00,0.000000000000000000e+00,3.000000000000000000e+00,4.000000000000000000e+00,0.000000000000000000e+00,3.879999999999999893e+00,3.890000000000000124e+00]]}' \
  -X POST http://localhost:8501/v1/models/user_embedding_model:predict



docker cp /tmp/user_embedding_model serving_base:/models/user_embedding_model

docker commit --change "ENV MODEL_NAME user_embedding_model" serving_base \
  user_embedding_model_serving

docker run -p 8501:8501 -t user_embedding_model_serving &

uvicorn server.main:app --host 127.0.0.1 --port 8000

docker build -t movie_recommender_python:v1 .

docker run --rm -p 80:80 movie_recommender_python:v1

# check tensor flow serving IP address in the bridge network
docker inspect gracious_volhard | grep IPAddress

docker-compose -f movieRec.yaml up

79e9f9fd5a221f85dc5e34e6ecdcdaf9adc718bb7bdfbbb5d9125911bf819a05
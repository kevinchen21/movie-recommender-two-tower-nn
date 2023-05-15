# Train and deploy a two-tower neural network recommendation system

In this repo, I will train a two tower neural network recommendation system and deploy it to a AWS EC2.

## data

The data set is derived from the MovieLens ml-latest-small dataset (https://grouplens.org/datasets/movielens/latest/).

## model architecture

I will build a two-tower neural network. One is to generate user embedding and the other is to generate item embedding. I will dot the user embedding and item embedding to predict the rating of the movie. This architeture is similar to JD's recommender system (https://arxiv.org/abs/2006.02282). After the model is trained, we will use the item network to pre-compute embeddings for all movies. We will deploy the user network to production and do real-time prediction for a given user. In the real-world application, we can take real-time features (searching word, browsing history, etc) to feed into the user network to generate real-time embedding for the user. We can use the user embedding to retrive top ranking items for this user.
<img width="497" alt="image" src="https://github.com/kevinchen21/train-and-deploy-nn-recsys/assets/87917613/27f25f1b-7a0c-4571-a960-e56e0a3381b9">

## model training

We will use identical network for both user and item. In real-world application, we can choose different architectures for the user and item network as long as the output embedding is same size. For this demo, I choose 3 layers sequential network, 256 units for the first layer, 128 units for the second, and 32 units as the output embedding. I will use the mean_square_error as the loss function, and the adam optimizer.

![image](https://github.com/kevinchen21/train-and-deploy-nn-recsys/assets/87917613/7a30e270-6392-49b4-a98b-1b396d78261a)

## server and inference

We will build a Rest API, using FastAPI. The server will take the user information as the input and generate the top 10 movies, based on the predicted ratings. I will use the KNN algorithm to retrive the top 10 movies.

## docker image
After we develop the server codes, we can build a docker image to integrate the server code. We can test the image by launching it in our local laptop.

## deploy to AWS

We can spin up a AWS EC2 and install the docker, by following this instruction (https://medium.com/bb-tutorials-and-thoughts/running-docker-containers-on-aws-ec2-9b17add53646). I will upload this image to AWS ECR and download it to the EC2 for running.



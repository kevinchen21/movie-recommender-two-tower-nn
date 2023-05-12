# Train and deploy a two-tower neural network recommendation system

In this repo, I will train a two tower neural network recommendation system and deploy it to a AWS EC2.

## data

The data set is derived from the MovieLens ml-latest-small dataset (https://grouplens.org/datasets/movielens/latest/).

## model architecture

I will build a two-tower neural network. One is to generate user embedding and the other is to generate item embedding. I will dot the user embedding and item embedding to predict the rating of the movie. This architeture is similar to JD's recommender system (https://arxiv.org/abs/2006.02282). After the model is trained, we will use the item network to pre-compute embeddings for all movies. We will deploy the user network to production and do real-time prediction for a given user. In the real-world application, we can take real-time features (searching word, browsing history, etc) to feed into the user network to generate real-time embedding for the user. We can use the user embedding to retrive top ranking items for this user.
<img width="497" alt="image" src="https://github.com/kevinchen21/train-and-deploy-nn-recsys/assets/87917613/27f25f1b-7a0c-4571-a960-e56e0a3381b9">

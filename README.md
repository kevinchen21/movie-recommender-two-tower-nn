# Train and deploy a two-tower neural network recommendation system

In this repo, I will show you how to train a deep learning model and deploy it to AWS EC2 and Kubernetes. I will train a two tower neural network recommendation system for movies. After we train the system, I will demo how to deploy it to a AWS EC2 and Kubernetes.

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

We will build two containers/images. One image is for the python code to take input (user id), and create features for the user embedding deep learning model. The second image use the tensorflow serving to serve the tensorflow model. 

In the two_conatiner folder, you can find the Dockerfile to build the python image.

For the tensorflow image, you can run the base tensorflow image, and then copy the user_embedding_model into the base image. See more detailed instructions in this tensoflow blog: https://www.tensorflow.org/tfx/serving/serving_kubernetes


## deploy to AWS EC2

We can spin up a AWS EC2 and install the docker, by following this instruction (https://medium.com/bb-tutorials-and-thoughts/running-docker-containers-on-aws-ec2-9b17add53646). We then can upload our python and tensorflow images to AWS ECR. Instructions on how to use ECR: https://www.youtube.com/watch?v=vWSRWpOPHws

## deploy to Kubernetes

In real application, this recommender system will serve as an API for internal user. It will run as a microservice, and other microservice can call this API to generate the recommended movies for different users. So I will create a Kubernetes cluster on AWS, using EKS and deploy the API to the Kubernetes cluster. I will deploy the API in two way. First, I'll deploy it using one pod for the python and tensorflow containers. The benefit is to reduce latency as these two containers in the same pod. Second, I'll deploy these two containers in two pods, using internal service to communicate between these two containers. It will take longer latency for the communication, but better for the resource optimization since these two containers are not tightly binded and the Kubernetes can optimize the resource allocation based on usage.

To launch the Kubernetes cluster, we will use eksctl command line to launch the cluster, with pre-defined yaml file (define the number of instances we need for this cluster). Here is the instruction on how to use eksctl: https://www.youtube.com/watch?v=p6xDCz00TxU&t=25s

As we already push the images to ECR, we can use kubectl to launch the API, using pre-defined deployment.yaml file. See the Kubernetes folder. For the one pod, it's quite straightforward. You only need to launch the deployment.yaml.

For the two pods case, you need to launch the tensorflow container first, and then the configmap to pass the tensorflow service address. Then you can launch the reommender container (python code).

## Latency test

The reommender system is a real-time application and requires low latency. We can use the locust (https://locust.io/) for latency test. You can launch the locust image, using the yaml file in the latency_test folder. The result shows the one pod setting is better than the two pods case. If we look into the local case where both the API and locust running in local host, the average latency is 12 ms compared to 180 ms when the API running in AWS Kubernetes.

<img width="1071" alt="image" src="https://github.com/kevinchen21/train-and-deploy-nn-recsys/assets/87917613/dd198fc1-1839-49fc-a216-b1a6b80b65cc">




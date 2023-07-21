from locust import HttpUser, task, constant


class LoadTest(HttpUser):
    wait_time = constant(0)
    host = "http://localhost"

    @task
    def predict_movie_local(self):
        request_body = {"uid": 2}
        self.client.post(
            "http://my-app:80/predict", json=request_body, name="movie_recommender_local"
        )
    
    @task
    def predict_movie_one_pod(self):
        request_body = {"uid": 2}
        self.client.post(
            "http://a816591493e694615a68a57087ed83aa-2035007287.us-west-2.elb.amazonaws.com:80/predict", json=request_body, name="movie_recommender_one_pod"
        )

    @task
    def predict_movie_two_pods(self):
        request_body = {"uid": 2}
        self.client.post(
            "http://a08dc185cd8884e2690dab30c0edfe49-325600394.us-west-2.elb.amazonaws.com:80/predict", json=request_body, name="movie_recommender_two_pods"
        )
    # @task
    # def predict_batch_32(self):
    #     request_body = {"batches": [[1.0 for i in range(13)] for i in range(32)]}
    #     self.client.post(
    #         "http://batch-32:80/predict", json=request_body, name="batch-32"
    #     )

    # @task
    # def predict_batch_64(self):
    #     request_body = {"batches": [[1.0 for i in range(13)] for i in range(64)]}
    #     self.client.post(
    #         "http://batch-64:80/predict", json=request_body, name="batch-64"
    #     )

    # @task
    # def predict_no_batch(self):
    #     request_body = {
    #         "alcohol": 1.0,
    #         "malic_acid": 1.0,
    #         "ash": 1.0,
    #         "alcalinity_of_ash": 1.0,
    #         "magnesium": 1.0,
    #         "total_phenols": 1.0,
    #         "flavanoids": 1.0,
    #         "nonflavanoid_phenols": 1.0,
    #         "proanthocyanins": 1.0,
    #         "color_intensity": 1.0,
    #         "hue": 1.0,
    #         "od280_od315_of_diluted_wines": 1.0,
    #         "proline": 1.0,
    #     }
    #     self.client.post(
    #         "http://no-batch:80/predict", json=request_body, name="0:batch"
    #     )
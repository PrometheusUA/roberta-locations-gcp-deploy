# Deployment task for UA locations extraction task

## Run
How to run it:
- Fill the environment file in the way `sample.env` is filled:
```
API_VERSION=v1

CHECKPOINT_PATH=checkpoints/...
DEVICE=cpu
```
- Create the environment: `conda create --name='ner-ua-deployment'`.
- Activate it: `conda activate ner-ua-deployment`.
- Install all the required dependencies: `pip install -r requirements.txt`.
- Start model by simply: `flask run`.

### Check that everything works

You can use `curl` locally:
```bash
curl -i -X POST -H "Content-Type: application/json" -d "{\"instances\":[\"Доброго вечора, ми з України\", \"У Києві мороз, трохи сніжить\"]}" http://localhost:5000/predict
```

## Deployment

How to deploy to Google Cloud Vertex AI:
- Create a GCP project and allow Vertex AI usage there.
- [Install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install#windows).
- Choose GCP region, create an Artifact registry docker repository there and allow Cloud build (on the Google Cloud Platform).
- Authenticate using: `gcloud auth application-default login` and your browser login.
- Send your model to the created Artifact Registry repository: `gcloud builds submit . --tag=YOUR-REGION-docker.pkg.dev/YOUR-PROJECT-ID/YOUR-REPOSITORY-NAME/nlp-ner-onnx-ua --machine-type='n1-highcpu-8' --timeout=900s --verbosity=info`
- After processing finish, use `deployment.ipynb` to finish setting it up.

*I wouldn't have deployed it without [this](https://medium.com/google-cloud/streamline-model-deployment-on-vertex-ai-using-onnx-65f29786d2d0) article.*

### Usage

You can also use the endpoint by:
1. Set up Python Google Cloud Platform client, if you haven't done this before.
2. Use the [sample Python file](https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py) to get a method of obtaining the predictions.
3. Execute the request like this:
```{python}
predict_custom_trained_model_sample(
    project=YOUR_PROJECT_ID,
    endpoint_id=YOUR_ENDPOINT_ID,
    location=YOUR_REGION,
    instances=texts
)
```

The result should be like this:

![Working model result](https://i.imgur.com/uZJpRJ8.png)

> Side note: I have also made an OpenAPI documentation, but it simply have no space to exist in the Google AI Platform. Probably, in this fassion it could also have been deployed on the Cloud Run to be much more accessible. At the same time, Google AI helps to monitor the model and to have it's checkpoints saved on the specific machine.

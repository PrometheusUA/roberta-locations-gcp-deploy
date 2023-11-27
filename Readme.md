# Deployment task for UA locations extraction task

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

How to deploy to Google Cloud Vertex AI:
- Create a GCP project and allow Vertex AI usage there.
- [Install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install#windows).
- Choose GCP region, create an Artifact registry docker repository there and allow Cloud build (on the Google Cloud Platform).
- Authenticate using: `gcloud auth application-default login` and your browser login.
- Send your model to the created Artifact Registry repository: `gcloud builds submit . --tag=YOUR-REGION-docker.pkg.dev/YOUR-PROJECT-ID/YOUR-REPOSITORY-NAME/nlp-ner-onnx-ua --machine-type='n1-highcpu-8' --timeout=900s --verbosity=info`
- After processing finish, use `deployment.ipynb` to finish setting it up.

import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from dotenv import load_dotenv

from schemas import InputSchema, OutputSchema
from models.location_predictor import LocationPredictor


DEFAULT_CHECKPOINT = 'PrometheusUA/roberta-distilled-quantized-ner-ua'

blp = Blueprint("NER", "ner", description="UA NER locations prediction")

@blp.route("/predict")
class NERPredict(MethodView):
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        self.predictor = LocationPredictor(os.environ.get("CHECKPOINT_PATH", DEFAULT_CHECKPOINT), os.environ.get("DEVICE", "cpu"))

    @blp.arguments(InputSchema)
    @blp.response(
        200, OutputSchema, description="Everything has gone good, the result is returned."
    )
    @blp.alt_response(400, description="Something went wrong")
    def post(self, texts):
        try:
            return {"predictions": self.predictor.predict(texts['instances'])}
        except Exception as e:
            abort(400, message=str(e))


@blp.route('/health')
class Healthcheck(MethodView):
    @blp.response(200, description="The server is up")
    def get(self):
        return dict(status="healthy")

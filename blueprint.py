import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import InputSchema, OutputSchema
from dotenv import load_dotenv

from location_predictor import LocationPredictor


blp = Blueprint("NER", "ner", description="UA NER locations prediction")

@blp.route("/predict")
class NERPredict(MethodView):
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        self.predictor = LocationPredictor(os.environ.get("CHECKPOINT_PATH"), os.environ.get("DEVICE"))

    @blp.arguments(InputSchema)
    @blp.response(
        200, OutputSchema, description="Everything has gone good, the result is returned."
    )
    @blp.alt_response(400, description="Something went wrong")
    def post(self, texts):
        try:
            return {"locations": self.predictor.predict(texts['texts'])}
        except Exception as e:
            abort(400, message=str(e))


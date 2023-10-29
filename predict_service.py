from quart import Quart, request, jsonify
import xgboost as xgb

# Quart app
app = Quart(__name__)


# Load xgboost model
xgb_model = xgb.XGBClassifier().load_model("models/xgboost_model.json")

# Connect the client before we start serving with Quart
@app.before_serving
async def startup():
    print("Starting star prediction service")

@app.after_serving
async def cleanup():
    print("Stopping star prediction service")

@app.route("/", methods=["GET"])
async def root():
    print("service running")

@app.route("/predict", methods=["POST"])
async def predict():
    object_features = request.get_json()
    feature_vector = []


if __name__ == "__main__":
    app.run(debug=True)
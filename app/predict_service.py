from quart import Quart, request, jsonify
import xgboost as xgb

# Quart app
app = Quart(__name__)

# Load xgboost model
star_model = xgb.XGBClassifier()
star_model.load_model("models/xgboost_model.json")

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
    object_features = await request.get_json()

    required_parameters = ["alpha", "delta", "u", "g", "r", "i","z","redshift"]
    pred_mapping = {
        0: "GALAXY",
        1: "STAR",
        2: "QSO"
    }

    if all([param in object_features for param in required_parameters]):
        feature_vector = [
            object_features["alpha"],
            object_features["delta"],
            object_features["u"],
            object_features["g"],
            object_features["r"],
            object_features["i"],
            object_features["z"],
            object_features["redshift"]
        ]
        predicted_label = star_model.predict([feature_vector])[0]
        predicted_class = pred_mapping.get(predicted_label, "UNKNOWN")        
        return jsonify({"prediction": predicted_class})
    else:
        return jsonify({"error": "Missing required parameters"}), 400    


if __name__ == "__main__":
    app.run(debug=True)
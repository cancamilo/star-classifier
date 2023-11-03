import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

# Import the data
df = pd.read_csv("data/star_classification.csv")

# Fiter out unnnecesary columns
position_columns = ["alpha", "delta"]
filter_columns = ["u", "g", "r", "i", "z","redshift"]
target_col = ["class"]
df = df[position_columns + filter_columns + target_col]

# Clean outliers
df = df[(df["u"] != -9999.0) & (df["g"] != -9999.0) & (df["z"] != -9999.0)]

print("Training model parameters: ")
print("""
    objective="multi:softprob", 
    colsample_bytree=0.798,
    random_state=42, 
    learning_rate=0.29, 
    gamma=0.0598, 
    max_depth=5, 
    n_estimators=124,
    subsample=0.877,
    eval_metric="auc",
    early_stopping_rounds=20
""")

# Initialize the model with previously optimized parameters
xgb_model = xgb.XGBClassifier(
    objective="multi:softprob", 
    colsample_bytree=0.798,
    random_state=42, 
    learning_rate=0.29, 
    gamma=0.0598, 
    max_depth=5, 
    n_estimators=124,
    subsample=0.877,
    eval_metric="auc",
    early_stopping_rounds=20
)

# Define prediction classes
map_class = {
    "GALAXY": 0,
    "STAR": 1,
    "QSO": 2
}

# Define features and target
df["target"] = df["class"].apply(lambda x: map_class[x])
X = df[position_columns + filter_columns]
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)

xgb_model.save_model("models/xgboost_model.json")

print("model saved to models/xgboost_model.json")
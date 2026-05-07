import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

FEATURE_COLUMNS = ["time_of_day", "zone_type", "congestion_level", "distance"]
TARGET_COLUMN = "delay_level"


# Trains a decision tree model on the dataset and returns the model,
# encoders, and accuracy.
def train_model(csv_path="data/robot_delay_data.csv"):
    data = pd.read_csv(csv_path)

    encoders = {}
    for column in data.columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        encoders[column] = le

    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))

    return model, encoders, accuracy


# Uses the trained model to predict delay level for a given route.
def predict_delay(model, encoders, time_of_day, zone_type, congestion_level, distance):
    sample = pd.DataFrame([{
        "time_of_day": encoders["time_of_day"].transform([time_of_day])[0],
        "zone_type": encoders["zone_type"].transform([zone_type])[0],
        "congestion_level": encoders["congestion_level"].transform([congestion_level])[0],
        "distance": encoders["distance"].transform([distance])[0],
    }])

    prediction = model.predict(sample)[0]
    return encoders[TARGET_COLUMN].inverse_transform([prediction])[0]


# Converts numeric distance (steps) into categorical labels for ML.
def categorize_distance(steps):
    if steps <= 20:
        return "short"
    elif steps <= 35:
        return "medium"
    else:
        return "long"

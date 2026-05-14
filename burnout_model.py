from sklearn.ensemble import IsolationForest


def get_risk_label(score):
    if score < 2:
        return "Low Risk"
    elif score < 5:
        return "Medium Risk"
    else:
        return "High Risk"


def compute_burnout_risk(df):
    df = df.copy()

    df["burnout_score"] = (
        df["late_night"] * 3
        + df["negative_score"] * 2
        + df["short_message"] * 1
    )

    features = df[
        [
            "hour",
            "message_length",
            "late_night",
            "negative_score",
            "short_message",
            "burnout_score",
        ]
    ]

    model = IsolationForest(
        contamination=0.1,
        random_state=42,
    )

    df["anomaly"] = model.fit_predict(features)

    df["anomaly_label"] = df["anomaly"].apply(
        lambda value: "Anomaly" if value == -1 else "Normal"
    )

    df["risk_level"] = df["burnout_score"].apply(get_risk_label)

    return df
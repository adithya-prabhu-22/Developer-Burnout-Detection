from sklearn.ensemble import IsolationForest


def get_risk_label(score):
    if score < 3:
        return "Low Risk"
    elif score < 7:
        return "Medium Risk"
    else:
        return "High Risk"


def compute_burnout_risk(df):
    df = df.copy()

    high_daily_activity = (df["daily_commit_frequency"] > 10).astype(int)
    long_gap = (df["inter_commit_gap_hours"] > 48).astype(int)
    very_small_diff = (df["total_changes"] < 5).astype(int)

    df["burnout_score"] = (
        df["late_night"] * 3
        + df["negative_score"] * 2
        + df["short_message"] * 1
        + high_daily_activity * 2
        + long_gap * 2
        + very_small_diff * 1
    )

    features = df[
        [
            "hour",
            "message_length",
            "late_night",
            "negative_score",
            "short_message",
            "inter_commit_gap_hours",
            "daily_commit_frequency",
            "weekly_commit_frequency",
            "additions",
            "deletions",
            "total_changes",
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
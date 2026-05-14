import pandas as pd


def calculate_negative_score(message):
    negative_words = [
        "fix", "bug", "broken", "fail", "failed", "failure",
        "urgent", "revert", "error", "issue", "issues", "crash",
        "hotfix", "patch", "hack", "temporary", "quickfix",
        "quick-fix", "debug", "debugging", "critical", "panic",
        "wrong", "bad", "unstable", "problem", "problems",
        "retry", "retrying", "broken again", "wtf", "stupid",
        "mess", "cleanup", "dirty", "ugly", "bypass",
        "exception", "fatal", "blocked", "blocking", "timeout",
        "timeouts", "leak", "memory leak", "cpu spike", "latency",
        "downtime", "rollback", "recovery", "broken build",
        "firefight", "refactor later", "temp", "temporary solution",
        "quick patch", "fix again", "again",
    ]

    message = str(message).lower()
    score = 0

    for word in negative_words:
        if word in message:
            score += 1

    return score


def create_features(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df = df.sort_values("date").reset_index(drop=True)

    df["hour"] = df["date"].dt.hour
    df["day"] = df["date"].dt.day_name()
    df["commit_date"] = df["date"].dt.date
    df["week"] = df["date"].dt.to_period("W").astype(str)

    df["message"] = df["message"].fillna("")
    df["message_length"] = df["message"].apply(len)

    df["late_night"] = df["hour"].apply(
        lambda hour: 1 if hour >= 22 or hour <= 4 else 0
    )

    df["negative_score"] = df["message"].apply(calculate_negative_score)

    df["short_message"] = df["message_length"].apply(
        lambda length: 1 if length < 20 else 0
    )

    df["inter_commit_gap_hours"] = (
        df["date"].diff().dt.total_seconds() / 3600
    ).fillna(0)

    df["daily_commit_frequency"] = (
        df.groupby("commit_date")["commit_date"].transform("count")
    )

    df["weekly_commit_frequency"] = (
        df.groupby("week")["week"].transform("count")
    )

    for column in ["additions", "deletions", "total_changes"]:
        if column not in df.columns:
            df[column] = 0

    return df
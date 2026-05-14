import streamlit as st
import matplotlib.pyplot as plt

from utils import extract_owner_repo
from github_fetcher import fetch_commits
from feature_engineering import create_features
from burnout_model import compute_burnout_risk


st.set_page_config(
    page_title="Developer Burnout Detection",
    layout="wide"
)

st.title("Developer Burnout Detection via Git Commit Mining")

st.write(
    "This app analyzes public GitHub repository commits and detects "
    "developer burnout risk patterns using data mining and anomaly detection."
)

repo_url = st.text_input(
    "Enter Public GitHub Repository URL",
    placeholder="https://github.com/pallets/flask"
)

max_pages = st.slider(
    "Number of GitHub API pages to fetch",
    min_value=1,
    max_value=10,
    value=3
)

if st.button("Analyze Repository"):

    owner, repo = extract_owner_repo(repo_url)

    if owner is None or repo is None:
        st.error("Invalid GitHub repository URL.")
        st.stop()

    with st.spinner("Fetching commits from GitHub..."):
        commits_df = fetch_commits(owner, repo, max_pages=max_pages)

    if commits_df is None or commits_df.empty:
        st.error("Could not fetch commits. Make sure the repository is public.")
        st.stop()

    features_df = create_features(commits_df)
    result_df = compute_burnout_risk(features_df)

    st.success("Analysis completed successfully.")

    total_commits = len(result_df)
    avg_burnout_score = result_df["burnout_score"].mean()
    late_night_percent = result_df["late_night"].mean() * 100
    anomaly_count = (result_df["anomaly"] == -1).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Commits", total_commits)
    col2.metric("Avg Burnout Score", round(avg_burnout_score, 2))
    col3.metric("Late Night Commits", f"{late_night_percent:.2f}%")
    col4.metric("Anomalies Detected", anomaly_count)

    if avg_burnout_score < 2:
        overall_risk = "Low Risk"
    elif avg_burnout_score < 5:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "High Risk"

    st.subheader(f"Overall Repository Burnout Risk: {overall_risk}")

    st.subheader("Burnout Risk Timeline")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(result_df.index, result_df["burnout_score"])
    ax.set_xlabel("Commit Number")
    ax.set_ylabel("Burnout Score")
    ax.set_title("Burnout Risk Over Commit Timeline")

    st.pyplot(fig)

    st.subheader("Commit Activity by Hour")

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    result_df["hour"].value_counts().sort_index().plot(
        kind="bar",
        ax=ax2
    )
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Number of Commits")
    ax2.set_title("Commit Distribution by Hour")

    st.pyplot(fig2)

    st.subheader("Risk Level Distribution")

    risk_counts = result_df["risk_level"].value_counts()

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    risk_counts.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Risk Level")
    ax3.set_ylabel("Number of Commits")
    ax3.set_title("Risk Level Distribution")

    st.pyplot(fig3)

    st.subheader("Anomalous Commits Detected by Isolation Forest")

    anomaly_df = result_df[result_df["anomaly"] == -1][
        [
            "date",
            "author",
            "message",
            "hour",
            "message_length",
            "negative_score",
            "burnout_score",
            "risk_level",
            "anomaly_label",
        ]
    ]

    st.dataframe(anomaly_df, use_container_width=True)

    st.subheader("Full Commit Analysis Data")

    st.dataframe(
        result_df[
            [
                "date",
                "author",
                "message",
                "hour",
                "day",
                "message_length",
                "late_night",
                "negative_score",
                "short_message",
                "burnout_score",
                "risk_level",
                "anomaly_label",
            ]
        ],
        use_container_width=True
    )

    st.warning(
        "Disclaimer: This system does not clinically diagnose burnout. "
        "It only detects behavioral risk patterns from Git commit activity."
    )
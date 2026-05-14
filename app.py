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
    "developer burnout risk patterns using data mining and Isolation Forest anomaly detection."
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


def clean_plot(ax):
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


if st.button("Analyze Repository"):

    owner, repo = extract_owner_repo(repo_url)

    if owner is None or repo is None:
        st.error("Invalid GitHub repository URL.")
        st.stop()

    with st.spinner("Fetching commits and diff statistics from GitHub..."):
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
    avg_gap = result_df["inter_commit_gap_hours"].mean()
    avg_diff_size = result_df["total_changes"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Commits", total_commits)
    col2.metric("Avg Burnout Score", round(avg_burnout_score, 2))
    col3.metric("Late Night Commits", f"{late_night_percent:.2f}%")
    col4.metric("Anomalies", anomaly_count)
    col5.metric("Avg Diff Size", round(avg_diff_size, 2))

    if avg_burnout_score < 3:
        overall_risk = "Low Risk"
    elif avg_burnout_score < 7:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "High Risk"

    st.subheader(f"Overall Repository Burnout Risk: {overall_risk}")

    st.divider()

    st.header("Behavioral Analytics Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Risk Timeline",
            "Commit Activity",
            "Diff Analysis",
            "Anomaly Report",
        ]
    )

    with tab1:
        st.subheader("Burnout Risk Timeline")

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(
            result_df["date"],
            result_df["burnout_score"],
            marker="o",
            linewidth=2,
            markersize=4,
        )
        ax.set_xlabel("Commit Date")
        ax.set_ylabel("Burnout Score")
        ax.set_title("Burnout Risk Over Time")
        clean_plot(ax)
        fig.autofmt_xdate()

        st.pyplot(fig)

        st.subheader("Risk Level Distribution")

        risk_counts = result_df["risk_level"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        risk_counts.plot(kind="bar", ax=ax2)
        ax2.set_xlabel("Risk Level")
        ax2.set_ylabel("Number of Commits")
        ax2.set_title("Distribution of Burnout Risk Levels")
        clean_plot(ax2)

        st.pyplot(fig2)

    with tab2:
        st.subheader("Commit Activity by Hour")

        hourly_counts = result_df["hour"].value_counts().sort_index()

        fig3, ax3 = plt.subplots(figsize=(12, 5))
        hourly_counts.plot(kind="bar", ax=ax3)
        ax3.set_xlabel("Hour of Day")
        ax3.set_ylabel("Number of Commits")
        ax3.set_title("Commit Distribution Across 24 Hours")
        clean_plot(ax3)

        st.pyplot(fig3)

        st.subheader("Daily Commit Frequency")

        daily_counts = (
            result_df.groupby("commit_date")
            .size()
            .reset_index(name="commit_count")
        )

        fig4, ax4 = plt.subplots(figsize=(12, 5))
        ax4.plot(
            daily_counts["commit_date"],
            daily_counts["commit_count"],
            marker="o",
            linewidth=2,
        )
        ax4.set_xlabel("Date")
        ax4.set_ylabel("Commit Count")
        ax4.set_title("Daily Commit Frequency")
        clean_plot(ax4)
        fig4.autofmt_xdate()

        st.pyplot(fig4)

        st.subheader("Inter-Commit Gap Over Time")

        fig5, ax5 = plt.subplots(figsize=(12, 5))
        ax5.plot(
            result_df["date"],
            result_df["inter_commit_gap_hours"],
            marker="o",
            linewidth=2,
            markersize=4,
        )
        ax5.set_xlabel("Commit Date")
        ax5.set_ylabel("Gap in Hours")
        ax5.set_title("Time Gap Between Consecutive Commits")
        clean_plot(ax5)
        fig5.autofmt_xdate()

        st.pyplot(fig5)

    with tab3:
        st.subheader("Diff Size Analysis")

        fig6, ax6 = plt.subplots(figsize=(12, 5))
        ax6.plot(
            result_df["date"],
            result_df["total_changes"],
            marker="o",
            linewidth=2,
            markersize=4,
        )
        ax6.set_xlabel("Commit Date")
        ax6.set_ylabel("Total Lines Changed")
        ax6.set_title("Diff Size Over Time")
        clean_plot(ax6)
        fig6.autofmt_xdate()

        st.pyplot(fig6)

        st.subheader("Additions vs Deletions")

        diff_summary = result_df[["additions", "deletions"]].sum()

        fig7, ax7 = plt.subplots(figsize=(7, 4))
        diff_summary.plot(kind="bar", ax=ax7)
        ax7.set_xlabel("Change Type")
        ax7.set_ylabel("Total Lines")
        ax7.set_title("Total Additions vs Deletions")
        clean_plot(ax7)

        st.pyplot(fig7)

    with tab4:
        st.subheader("Anomalous Commits Detected by Isolation Forest")

        anomaly_df = result_df[result_df["anomaly"] == -1][
            [
                "date",
                "author",
                "message",
                "hour",
                "inter_commit_gap_hours",
                "daily_commit_frequency",
                "weekly_commit_frequency",
                "additions",
                "deletions",
                "total_changes",
                "negative_score",
                "burnout_score",
                "risk_level",
                "anomaly_label",
            ]
        ]

        st.dataframe(anomaly_df, use_container_width=True)

    st.divider()

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
                "inter_commit_gap_hours",
                "daily_commit_frequency",
                "weekly_commit_frequency",
                "additions",
                "deletions",
                "total_changes",
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
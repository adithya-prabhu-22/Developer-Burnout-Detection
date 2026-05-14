import requests
import pandas as pd


def fetch_commit_details(owner, repo, sha):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"

    response = requests.get(api_url)

    if response.status_code != 200:
        return {
            "additions": 0,
            "deletions": 0,
            "total_changes": 0,
        }

    data = response.json()
    stats = data.get("stats", {})

    return {
        "additions": stats.get("additions", 0),
        "deletions": stats.get("deletions", 0),
        "total_changes": stats.get("total", 0),
    }


def fetch_commits(owner, repo, max_pages=3):
    commits = []

    for page in range(1, max_pages + 1):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"

        params = {
            "per_page": 100,
            "page": page,
        }

        response = requests.get(api_url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            break

        for item in data:
            sha = item.get("sha")
            commit = item.get("commit", {})
            author = commit.get("author", {})

            diff_stats = fetch_commit_details(owner, repo, sha)

            commits.append({
                "sha": sha,
                "author": author.get("name", "Unknown"),
                "date": author.get("date"),
                "message": commit.get("message", ""),
                "additions": diff_stats["additions"],
                "deletions": diff_stats["deletions"],
                "total_changes": diff_stats["total_changes"],
            })

    return pd.DataFrame(commits)
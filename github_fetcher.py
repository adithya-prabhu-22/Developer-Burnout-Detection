import requests
import pandas as pd


def fetch_commits(
    owner,
    repo,
    max_pages=3,
):
    """
    Fetch commit history from a public GitHub repository.

    Returns:
        pandas DataFrame
    """

    commits = []

    for page in range(1, max_pages + 1):

        api_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/commits"
        )

        params = {
            "per_page": 100,
            "page": page,
        }

        response = requests.get(
            api_url,
            params=params,
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            break

        for item in data:

            commit = item.get("commit", {})
            author = commit.get("author", {})

            commits.append({
                "author": author.get(
                    "name",
                    "Unknown"
                ),

                "date": author.get(
                    "date"
                ),

                "message": commit.get(
                    "message",
                    ""
                ),
            })

    df = pd.DataFrame(commits)

    return df
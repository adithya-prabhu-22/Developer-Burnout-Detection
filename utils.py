import re


def extract_owner_repo(repo_url):
    """
    Extract owner and repository name from a GitHub repository URL.

    Example:
    https://github.com/pallets/flask
    returns: ("pallets", "flask")
    """

    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, repo_url)

    if not match:
        return None, None

    owner = match.group(1)
    repo = match.group(2).replace(".git", "")

    return owner, repo
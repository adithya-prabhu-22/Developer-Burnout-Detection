files = [
    "app.py",
    "github_fetcher.py",
    "feature_engineering.py",
    "burnout_model.py",
    "utils.py",
    "requirements.txt",
    "Dockerfile",
    "README.md",
    ".gitignore"
]

for file in files:

    with open(file, "w") as f:
        pass

print("Project structure created successfully.")
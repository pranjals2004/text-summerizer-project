from pathlib import Path

import setuptools

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

__version__ = "0.0.0"
REPO_NAME = "text-summerizer-project"
AUTHOR_USER_NAME = "pranjals2004"
SRC_REPO = "textSummarizer"
AUTHOR_EMAIL = "sharmapranjal80133@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small package for NLP app",
    long_description=README,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)

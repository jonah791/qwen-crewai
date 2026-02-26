"""Setup configuration for CrewAI framework"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="crewai_framework",
    version="0.1.0",
    author="CrewAI Developer",
    description="A multi-agent collaboration framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/crewai_framework",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "black>=21.0", "flake8>=3.8"],
    },
)

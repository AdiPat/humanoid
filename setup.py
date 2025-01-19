from setuptools import setup, find_packages

setup(
    name="humanoid",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy==1.26.4",
        "pandas==1.5.3",
        "python-dotenv==1.0.1",
        "pydantic==2.10.4",
        "pydantic-settings==2.7.1",
        "pydantic_core==2.27.2",
        "crewai==0.95.0",
        "crewai-tools==0.25.8",
    ],
    author="Aditya Patange (AdiPat)",
    author_email="contact.adityapatange@gmail.com",
    description="A system to configure, setup and run autonomous AI agents using natural language.",
    url="https://github.com/AdiPat/humanoid",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

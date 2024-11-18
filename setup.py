from setuptools import setup, find_packages

setup(
    name="raft",
    version="0.1.0",
    description="Retrieval-Augmented Fine-Tuning",
    author="lumpenspace",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.12.3",
        "chromadb==0.5.18",
        "openai>=1.14.3",
        "requests>=2.31.0",
        "tiktoken>=0.6.0",
        "pandas>=2.2.1",
        "pynput>=1.7.6",
    ],
    entry_points={
        "console_scripts": [
            "raft=raft.cli:main",
        ],
    },
)

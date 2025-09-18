from setuptools import setup, find_packages

setup(
    name="Qryptalk",
    version="0.1.0",
    author="QrypTalk Development Team",
    description="Post-Quantum Secure Messaging Application",
    packages=find_packages(),
    install_requires=[
        "pqcrypto==0.1.8",
        "cryptography==41.0.0",
        "PyQt6==6.5.0",
        "sqlcipher3==0.5.0",
        "websockets==11.0.0",
        "keyring==24.0.0",
        "pytest",
        "bandit",
        "safety",
        "black",
        "flake8",
        "mypy",
        "sphinx"
    ],
    entry_points={
        "console_scripts": [
            "qryptalk=Qryptalk.main:main"
        ]
    },
    python_requires='>=3.9',
)

from setuptools import setup, find_packages

setup(
    name="whatsapp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "annotated-types>=0.6.0",
        "anyio>=4.2.0",
        "asyncio>=3.4.3",
        "certifi>=2023.11.17",
        "charset-normalizer>=3.3.2",
        "click>=8.1.7",
        "fastapi>=0.109.0",
        "h11>=0.14.0",
        "httpcore>=1.0.2",
        "httpx>=0.25.2",
        "idna>=3.6",
        "iniconfig>=2.0.0",
        "packaging>=23.2",
        "pluggy>=1.4.0",
        "pydantic>=2.5.3",
        "pydantic_core>=2.14.6",
        "pytest>=7.4.4",
        "pytest-asyncio>=0.23.3",
        "pytest-mock>=3.12.0",
        "python-dotenv>=1.0.1",
        "requests>=2.31.0",
        "sniffio>=1.3.0",
        "starlette>=0.35.1",
        "typing_extensions>=4.9.0",
        "urllib3>=2.1.0",
        "uvicorn>=0.27.0",
    ],
)

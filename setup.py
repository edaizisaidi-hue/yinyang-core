from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yinyang-dialectics",
    version="1.0.0",
    description="Yin-Yang Recursive Dialectic Detector - AI Safety & Injection Prevention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="edaizisaidi-hue",
    author_email="edaizisaidi@gmail.com",
    url="https://github.com/edaizisaidi-hue/yinyang-core",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
        "api": [
            "fastapi>=0.95.0",
            "uvicorn>=0.21.0",
            "python-dotenv>=1.0.0",
            "pydantic>=2.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Security",
    ],
    keywords="security ai-safety jailbreak-detection injection-prevention yin-yang adversarial",
    project_urls={
        "Bug Reports": "https://github.com/edaizisaidi-hue/yinyang-core/issues",
        "Source": "https://github.com/edaizisaidi-hue/yinyang-core",
        "Documentation": "https://github.com/edaizisaidi-hue/yinyang-core/wiki",
    },
)

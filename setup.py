from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-video-generator",
    version="2.0.0",
    author="AI Video Generation Platform",
    author_email="contact@example.com",
    description="Professional AI video generation with advanced visual effects and viral-ready hooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-video-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Content Creators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.11",
    install_requires=[
        "Flask>=2.3.3",
        "Werkzeug>=2.3.7",
        "gunicorn>=21.2.0",
        "SQLAlchemy>=2.0.23",
        "Flask-SQLAlchemy>=3.1.1",
        "psycopg2-binary>=2.9.9",
        "Pillow>=10.1.0",
        "requests>=2.31.0",
        "opencv-python>=4.8.1.78",
        "numpy>=1.24.4",
        "scipy>=1.11.4",
        "moviepy>=1.0.3",
        "email-validator>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-video-generator=main:main",
        ],
    },
    keywords="ai video generation flask opencv visual-effects",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-video-generator/issues",
        "Source": "https://github.com/yourusername/ai-video-generator",
        "Documentation": "https://github.com/yourusername/ai-video-generator/wiki",
    },
)
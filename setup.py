from setuptools import setup

setup(
    name= "grammar_translator",
    version= "0.1",
    packages= ["grammar_translator"],
    install_requires= [
            "spacy",
            "es_core_news_sm @ https://github.com/explosion/spacy-models/releases/download/es_core_news_sm-3.4.0/es_core_news_sm-3.4.0.tar.gz"
    ],
    extras_require= {
        "dev": [
                "pytest",
                "jupyterlab"]
        }
)
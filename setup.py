from setuptools import setup

setup(
    name= "grammar_translator",
    version= "0.1",
    packages= ["grammar_translator"],
    install_requires= [
            "spacy",
            "es_core_web_md @ https://github.com/explosion/spacy-models/releases/download/es_core_web_md-1.0.0/es_core_web_md-1.0.0.tar.gz"
    ],
    extras_require= {
        "dev": [
                "pytest",
                "jupyterlab"]
        }
)
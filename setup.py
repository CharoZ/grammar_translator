from setuptools import setup

setup(
    name= "grammar_translator",
    version= "0.1",
    packages= ["grammar_translator"],
    install_requires= [],
    extras_require= {
        "dev": ["pytest"]
        }
)
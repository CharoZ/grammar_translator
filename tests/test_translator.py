import pytest
from unittest.mock import MagicMock
from grammar_translator import translator

@pytest.fixture
def mock_categorial():
    gram = """:- S, NP, NC, PARTP, PP
            D :: NP/NC
            PRO :: NP

            TV :: (S\\NP)/NP
            DTV :: TV/PP


            el => D
            la => D
            una => D
            un => D

            julia => NP
            cata => NP
            fede => NP
            martín => NP
            pablo => NP
            fer => NP
            vicky => NP

            él => PRO
            ella => PRO

            regalo => NC
            globo => NC
            plaza => NC
            facultad => NC
            tabaco => NC

            fuma => S\\NP

            fumo => TV
            exploto => TV

            envio => DTV
            entrego => DTV

            a => PP/NP
            por => PP/NP
            en => PP/NP

            fumado => PARTP/PP
            enviado => PARTP/PP
            entregado => PARTP/PP
            explotado => PARTP/PP

            fue => (S\\NP)/PARTP

            exploto => S\\NP
            habla => S\\NP
    """
    return gram

@pytest.fixture
def hacer_spacy_token():
    def hacer_token(palabra):
        mapeo =  {
            "julia": "PROPN",
            "pelota": "NOUN",
            "corre": "VERB",
            "entregado": "VERB", 
            "en": "ADP",
            "una": "DET",
            "ella": "PRON",
            "la": "DET",
            "fue": "AUX",
            "palabranoencontrada": "cat no mapeada"
        }
        token = MagicMock()
        token.pos_ = mapeo[palabra]
        if palabra == "entregado":
            token.morph = ["lala:Part"]
        elif palabra == "corre":
            token.morph = [" "]
        return token
    return hacer_token

@pytest.fixture
def monkeypatch_carga_modelo(monkeypatch):
    def carga_mock(nombre_modelo):
        def nlp_mock(palabra):
            token_mock = MagicMock()
            token_mock.text = palabra
            return [token_mock]
        return nlp_mock
    monkeypatch.setattr(translator.spacy, 'load', carga_mock)

@pytest.fixture
def monkeypatch_busqueda_de_categoria(monkeypatch):
    def busqueda_mock(token_terminal):
        mapeo =  {
            "julia": "NP",
            "pelota": "NC",
            "corre": "V",
            "entregado": "PART", 
            "en": "P",
            "una": "D",
            "ella": "PRO",
            "la": "D",
            "fue": "AUX",
            "palabranoencontrada": None
        }
        return mapeo[token_terminal.text]
    monkeypatch.setattr(translator, 'busqueda_de_categoria', busqueda_mock)

def test_preprocesamiento(mock_categorial):
    esperado = [         
            "julia",
            "cata",
            "fede",
            "martín",
            "pablo",
            "fer",
            "vicky",
            "fuma",
            "él",
            "ella",
            "fumo",
            "exploto",
            "a",
            "por",
            "en",
            "exploto",
            "habla",                
            "regalo",
            "globo",
            "plaza",
            "facultad",
            "tabaco",
            "el",
            "la" ,
            "una",
            "un",
            "envio",
            "entrego",
            "fumado",
            "enviado",
            "entregado",
            "explotado",            
            "fue"
        ]
    resultado = translator.preprocesamiento(mock_categorial)
    assert set(resultado) == set(esperado)

@pytest.mark.parametrize('terminal, output_esperado', [
    (
        "julia",
        "NP"
    ),
    (
        "pelota",
        "NC"
    ),
    (
        "corre",
        "V"

    ),
    (
        "entregado",
        "PART"
    ),
    (
        "en",
        "P"
    ),
    (
        "una",
        "D"
    ), 
    (
        "ella",
        "PRO"
    ),
    (
        "la",
        "D"
    ),
    (
        "fue",
        "AUX"
    ),
    (
        "palabranoencontrada",
        None
    )
])
def test_busqueda_de_categoria(hacer_spacy_token,terminal, output_esperado):
    token = hacer_spacy_token(terminal)
    output = translator.busqueda_de_categoria(token)
    assert output_esperado == output

@pytest.mark.parametrize('terminales, output_esperado', [
    (
        [
            "julia",
            "pelota",
            "corre",
            "entregado", 
            "en",
            "una",
            "ella",
            "la",
            "fue",
            "palabranoencontrada"
        ],
        (
            {
                "julia": "NP",
                "pelota": "NC",
                "corre": "V",
                "entregado": "PART", 
                "en": "P",
                "una": "D",
                "ella": "PRO",
                "la": "D",
                "fue": "AUX"
            },
            {
                "NP",
                "NC",
                "V",
                "PART",
                "P",
                "D",
                "PRO",
                "AUX"
            }
        )
    ),
    (
        list(),
        (
            dict(),
            set()
        )
    )
])
def test_traduccion_terminales(monkeypatch_carga_modelo, monkeypatch_busqueda_de_categoria, terminales, output_esperado):
    traduccion = translator.traduccion_terminales(terminales)
    output = (traduccion[0], set(traduccion[1]))
    assert output == output_esperado
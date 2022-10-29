import pytest
from unittest.mock import MagicMock
from grammar_translator import traductor

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
    monkeypatch.setattr(translator.spacy, "load", carga_mock)

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
    monkeypatch.setattr(translator, "busqueda_de_categoria", busqueda_mock)

@pytest.fixture
def monkeypatch_buscador_de_reglas(monkeypatch):
    def buscador_mock(simbolos, banco):
        reglas = []
        keys = []
        if "D" in simbolos:
            reglas.append("SN -> D NC SP")
            reglas.append("SN -> D NC")
            keys.append("SN")
        if "NP" in simbolos: 
            reglas.append("SN -> NP")
            keys.append("SN")
        if "SN" in simbolos:
            reglas.append("O -> SN SV")
            keys.append("O")
        return reglas, keys
    monkeypatch.setattr(translator, "buscador_de_reglas", buscador_mock)

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

@pytest.mark.parametrize("terminal, output_esperado", [
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

@pytest.mark.parametrize("terminales, output_esperado", [
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

@pytest.mark.parametrize("simbolos, output_esperado", [
    (
        [
            "SN",
            "V"
        ],
        (
            set([
                "FV -> V",
                "SP -> P SN"
            ]),
            set([
                "FV",
                "SP"
            ])
        )
    ),
    (
        [
            "D",
            "NP"
        ],
        (
            set(),
            set()
        )
    ),
    (
        list(),
        (
            set(),
            set()
        )
    )
])
def test_buscador_de_reglas(simbolos, output_esperado):
    banco_mock = {
        "FV":[
            "AUX PART",
            "V"
            ],   
        "SP":[
            "P SN"
            ]
        }
    output = translator.buscador_de_reglas(simbolos, banco_mock)
    assert (set(output[0]), set(output[1])) == output_esperado

@pytest.mark.parametrize("simbolos, output_esperado", [
    (
        [
            "D",
            "NP"
        ],
        [
            "SN -> D NC SP",
            "SN -> D NC",
            "SN -> NP",
            "O -> SN SV"
        ]
    ),
    (
        [
            "V",
            "NP"
        ],
        [
            "SN -> NP",
            "O -> SN SV"
        ]
    ),
    (
        [
            "H",
            "G"
        ],
        list()
    ),
    (
        list(),
        list()
    )
]
)
def test_creacion_gramatica(monkeypatch_buscador_de_reglas, simbolos, output_esperado):
    banco_mock = {
        "O":[
            "SN SV"
        ],
        "SN":[
            "PRO",
            "NP",
            "D NC",
            "D NC SP"
        ]
        }
    output = translator.creacion_gramatica(simbolos, banco_mock)
    assert set(output) == set(output_esperado)

@pytest.mark.parametrize('reglas, terminales_taggeados, output_esperado', [
    (["S -> SN SV", "SN -> PRO", "SN -> D NC", "SN -> NP", "SV -> FV", "FV -> DTV"],
     {"Julia": "NP", "regalo": "NC","globo": "NC", "ella": "PRO", "el": "D", "envió": "DTV"}, 
     ["S -> SN SV", "SN -> PRO", "SN -> D NC", "SN -> NP", "SV -> FV", "FV -> DTV", "NP -> 'Julia'", "NC -> 'regalo' | 'globo'", "PRO -> 'ella'", "D -> 'el'", "DTV -> 'envió'"])
])
def test_unificacion_de_reglas(reglas, terminales_taggeados, output_esperado):
    output = translator.unificacion_de_reglas(reglas,terminales_taggeados)
    assert set(output_esperado) == set(output)
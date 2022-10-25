import pytest
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

def test_given_categorial_grammar_when_translator_runs_then_return_CFG(mock_categorial, expected):
    expected = """S -> SN SV
            SN -> PRO
            SN -> D NC
            SN -> NP
            NP ->  'julia' | 'cata' | 'fede' | 'martín' | 'pablo' | 'fer' | 'vicky'
            NC -> 'regalo' | 'globo' | 'plaza' | 'facultad' | 'tabaco'
            D -> 'el' | 'la' | 'una' | 'un'
            PRO -> 'él' | 'ella'
            PART -> 'enviado' | 'entregado' | 'explotado' | 'fumado'
            IV -> 'fuma' | 'habla'
            TV -> 'fumo' | 'exploto'
            DTV -> 'envio' | 'entrego'
            SV -> TV SN
            SV -> DTV SN
            SV -> DTV SN SN
            SV -> IV
            SV -> FV
            SV -> FV SP
            SV -> FV SN
            FV -> AUX PART
            FV -> DTV
            AUX -> 'fue'
            SP -> P SN
            P -> 'a' | 'por' | 'en'
    """
    result = translator(mock_categorial)
    assert result == expected

def test_given_categorial_grammar_when_preprocesamiento_runs_then_return_preprocessed(mock_categorial):
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

@pytest.mark.parametrize('terminales, output_esperado', [
    (["julia", "pelota", "corre", "entregado", "en", "una", "ella", "la", "fue"],
    ["NP", "NC", "V", "PART", "P", "D", "PRO", "D", "AUX"]
    ),
    (["julia", "pelota", "corre", "enrtegado", "en", "una", "ella", "la", "fue"],
    ["NP", "NC", "V", "P", "D", "PRO", "D", "AUX"])
])
def test_traductor_simbolos_terminales(terminales, output_esperado):
    output = translator.traductor_simbolos_terminales(terminales)
    assert output_esperado == output

@pytest.mark.parametrize('reglas, terminales_taggeados, output_esperado', [
    (['S -> SN SV', 'SN -> PRO', 'SN -> D NC', 'SN -> NP', 'SV -> FV', 'FV -> DTV'],
     {'regalo': 'NC', 'Julia': 'NP', 'NC': 'globo', 'PRO': 'él', 'D': 'el', 'DTV': 'envió'}, 
     ['S -> SN SV', 'SN -> PRO', 'SN -> D NC', 'SN -> NP', 'SV -> FV', 'FV -> DTV', 'NC -> \'Julia\'', 'NC -> \'regalo\'', 'NC -> \'globo\'', 'PRO -> \'él\'', 'D -> \'el\'', 'DTV -> \'envió\''])
])
    
def test_unificacion_de_reglas(reglas, terminales_taggeados, output_esperado):
    output = translator.unificacion_de_reglas(reglas,terminales_taggeados)
    assert output_esperado == output
import pytest
from grammar_translator import translator 

@pytest.mark.parametrize('grammar, expected', [
    (
        """:- S, NP, NC, PARTP, PP
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

            fumó => TV
            explotó => TV

            envió => DTV
            entregó => DTV

            a => PP/NP
            por => PP/NP
            en => PP/NP

            fumado => PARTP/PP
            enviado => PARTP/PP
            entregado => PARTP/PP
            explotado => PARTP/PP

            fue => (S\\NP)/PARTP

            explotó => S\\NP
            habla => S\\NP
            """,
        """S -> SN SV
            SN -> PRO
            SN -> D NC
            SN -> NP
            NP ->  'julia' | 'cata' | 'fede' | 'martín' | 'pablo' | 'fer' | 'vicky'
            NC -> 'regalo' | 'globo' | 'plaza' | 'facultad' | 'tabaco'
            D -> 'el' | 'la' | 'una' | 'un'
            PRO -> 'él' | 'ella'
            PART -> 'enviado' | 'entregado' | 'explotado' | 'fumado'
            IV -> 'fuma' | 'habla'
            TV -> 'fumó' | 'explotó'
            DTV -> 'envió' | 'entregó'
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
            P -> 'a' | 'por' | 'en'"""
    )
])
def test_orquestadora(grammar, expected):
    result = translator.orquestadora(grammar)
    assert result == expected


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
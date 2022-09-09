def preprocesamiento(gramatica_categorial):
    '''
        Funcion que preprocesa la gramatica categorial. Devuelve
        simbolos terminales.
        Parametros
        ----------
        gramtica_categorial: str
            Gramatica para preprocesar.
            
        Returns
        -------
        lista_terminales: list
            Lista con los simbolos terminales de la gramatica.
    '''
    lineas = gramatica_categorial.split('\n')
    primer_simbolo = [p.split(' =>')[0] for p in lineas]
    lista_terminales = [p for p in primer_simbolo if not p.isupper()]
    return lista_terminales
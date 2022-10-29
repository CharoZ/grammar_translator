from grammar_translator import traductor
import argparse

if __name__ == "__main__":
    parser = ArgumentParser(description="")
    parser.add_argument("archivo", 
                        metavar="FILE", 
                        type= str, 
                        help="Indicar el nombre del archivo a traducir")
    parser.add_argument("idioma", 
                        metavar="LAN", 
                        nargs="?", 
                        type= str, 
                        default= "es", 
                        help="Seleccionar el idioma")
    parser.add_argument("gramatica", 
                        metavar="GRAMMAR", 
                        nargs="?", 
                        type= str, 
                        default= "cfg", 
                        help="Seleccionar el tipo de gramática")

    args = parser.parse_args()

    traductor.traduccion_gramatica(args.archivo, args.idioma, args.gramatica)
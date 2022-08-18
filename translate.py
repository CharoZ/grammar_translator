from grammar_translator import translator
import argparse

if __name__ == "__main__":
    parser = ArgumentParser(description="")
    parser.add_argument("file", 
                        metavar="FILE", 
                        type= str, 
                        help="Indicar el nombre del archivo a traducir")
    parser.add_argument("language", 
                        metavar="LAN", 
                        nargs="?", 
                        type= str, 
                        default= "es", 
                        help="Seleccionar el idioma")
    parser.add_argument("grammar", 
                        metavar="GRAMMAR", 
                        nargs="?", 
                        type= str, 
                        default= "cfg", 
                        help="Seleccionar el tipo de gramàtica")

    args = parser.parse_args()

    translator.translate(args.source, args.language, args.grammar)
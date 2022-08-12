from grammar_translator import translator
import argparse

if __name__ == "__main__":
    parser = ArgumentParser(description="")
    parser.add_argument("source", 
                        metavar="SOURCE", 
                        nargs="+", #creo que ? lo hace optativo 
                        type= str, 
                        #action= "store_true", #no me acuerdo que hace
                        #default= "", #no es obligatorio
                        help="Indicar el nombre del archivo a traducir")
    parser.add_argument("language", 
                        metavar="LAN", 
                        nargs="?", #creo que ? lo hace optativo
                        type= str, 
                        #action= "store_true", #no me acuerdo que hace
                        default= "es", #no es obligatorio
                        help="Seleccionar el idioma")
    parser.add_argument("grammar", 
                        metavar="GRAMMAR", 
                        nargs="?", #creo que ? lo hace optativo 
                        type= str, 
                        #action= "store_true", #no me acuerdo que hace
                        default= "cfg", #no es obligatorio
                        help="Seleccionar el tipo de gramàtica")

    args = parser.parse_args()

    translator.translate(args.source, args.language, args.grammar)
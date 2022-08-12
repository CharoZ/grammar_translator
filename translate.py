from grammar_translator import translator
import argparse

if __name__ == "__main__":
    parser = ArgumentParser(description="")
    parser.add_argument("", 
                        metavar="", 
                        nargs="+/?", #creo que ? lo hace optativo
                        choices=[], 
                        type= str, 
                        #action= "store_true", #no me acuerdo que hace
                        #default= "", #no es obligatorio
                        help="")

    args = parser.parse_args()    #desde acà se llama como args.variable
#for making samples, will go away when functionality exists
import sys

with open(sys.argv[1], "rb") as f:
    data = f.read()
    print data.encode("base64")
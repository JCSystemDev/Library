# Menú Principal de la aplicación

import pymongo
import tkinter

mongoHost = "localhost"
mongoPort = "27017"
mongoTimeout = 1000
mongoUrl = "mongodb://"+mongoHost+":"+mongoPort+"/"

try:
    client = pymongo.MongoClient(mongoUrl, serverSelectionTimeoutMS = mongoTimeout)
    client.server_info()
    print("Conexión a Mongo exitosa")
    client.close()
except pymongo.errors.ServerSelectionTimeoutMS as errorTime:
    print("Tiempo Excedido "+errorTime)
except pymongo.errors.ConnectionFailure as errorConnection:
    print("Fallo al conectarse a MongoDB"+errorConnection)



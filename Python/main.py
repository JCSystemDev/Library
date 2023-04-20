# Menú Principal de la aplicación
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo

mongoHost = "localhost"
mongoPort = "27017"
mongoTimeout = 1000
mongoUrl = "mongodb://"+mongoHost+":"+mongoPort+"/"
mongo_db = "tienda"
mongo_collection = "usuario"

def displayDocuments(table):
    try:
        client = pymongo.MongoClient(mongoUrl, serverSelectionTimeoutMS = mongoTimeout)
        client.server_info()
        print("Conexión a Mongo exitosa\n")
        dataBase = client[mongo_db]
        collection = dataBase[mongo_collection]
        print("Nombre de usuarios:\n")
        for document in collection.find():
            table.insert('', 0,text=document["user"],values=document["email"])
            print("Nombre: "+document["name"]+" "+document["lastname"]+" / Email: "+document["email"])
        print()
        client.close()
    except pymongo.errors.ServerSelectionTimeoutMS as errorTime:
        print("Tiempo Excedido "+errorTime)
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Fallo al conectarse a MongoDB"+errorConnection)


#Interfaz gráfica

window = Tk()
table = ttk.Treeview(window, columns=2)
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="Nombre de Usuario")
table.heading("#1", text="Email")
displayDocuments(table)
window.mainloop()
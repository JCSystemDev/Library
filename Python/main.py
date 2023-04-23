# Menú Principal de la aplicación
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

mongoHost = "localhost"
mongoPort = "27017"
mongoTimeout = 1000
mongoUrl = "mongodb://"+mongoHost+":"+mongoPort+"/"
mongo_db = "tienda"
mongo_collection = "usuario"
client = pymongo.MongoClient(mongoUrl, serverSelectionTimeoutMS = mongoTimeout)
dataBase = client[mongo_db]
collection = dataBase[mongo_collection]
id_user = ""

def displayDocuments(usuario="",correo=""):
    objectSearch={}
    if len(usuario)!=0:
        objectSearch["user"]=usuario
    if len(correo)!=0:
        objectSearch["email"]=correo
    try:
        rows = table.get_children()
        for row in rows:
            table.delete(row)
        for document in collection.find(objectSearch):
            table.insert('', 0,text=document["_id"],values=document["user"])
    except pymongo.errors.ServerSelectionTimeoutMS as errorTime:
        print("Tiempo Excedido"+errorTime)
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Fallo al conectarse a MongoDB"+errorConnection)

def insertData():
    if len(usuario.get())!=0 and len(clave.get())!=0 and len(nombre.get())!=0 and len(apellido.get())!=0 and len(correo.get())!=0 :
        try:
            document = {"user":usuario.get(), "password":clave.get(),"name":nombre.get(), "lastname":apellido.get(),"email":correo.get()}
            collection.insert_one(document)
            usuario.delete(0, END)
            clave.delete(0, END)
            nombre.delete(0, END)
            apellido.delete(0, END)
            correo.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacíos")
    displayDocuments()

def updateData():
    global id_user
    if len(usuario.get())!=0 and len(clave.get())!=0 and len(nombre.get())!=0 and len(apellido.get())!=0 and len(correo.get())!=0:
        try:
            idSearch={"_id":ObjectId(id_user)}
            updatedValues={"$set":{"user":usuario.get(), "password":clave.get(), "name":nombre.get(), "lastname":apellido.get(), "email":correo.get()}}
            collection._update_retryable(idSearch, updatedValues)
            usuario.delete(0,END)
            clave.delete(0,END)
            nombre.delete(0,END)
            apellido.delete(0,END)
            correo.delete(0,END)      
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacíos")
        
    displayDocuments()        
    insert["state"]="normal"
    update["state"]="disabled"
    delete["state"]="disabled"

def deleteData():
    global id_user
    try:
        idSearch={"_id":ObjectId(id_user)}
        collection.delete_one(idSearch)
        usuario.delete(0,END)
        clave.delete(0,END)
        nombre.delete(0,END)
        apellido.delete(0,END)
        correo.delete(0,END)     
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    insert["state"]="normal"
    update["state"]="disabled"
    delete["state"]="disabled"
    displayDocuments()

def searchData():
    displayDocuments(buscarUsuario.get(), buscarCorreo.get())

def doubleClickTable(event):
    global id_user
    id_user = str(table.item(table.selection())["text"])
    document = collection.find({"_id":ObjectId(id_user)})[0]
    usuario.delete(0,END)
    usuario.insert(0, document["user"])
    clave.delete(0,END)
    clave.insert(0, document["password"])
    nombre.delete(0,END)
    nombre.insert(0, document["name"])
    apellido.delete(0,END)
    apellido.insert(0, document["lastname"])
    correo.delete(0,END)
    correo.insert(0, document["email"])
    insert["state"]="disabled"
    update["state"]="normal"
    delete["state"]="normal"



#Interfaz gráfica
window = Tk()
window.configure(bg="black")
window.title("Registro de usuarios")
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", background="black", foreground="white")
table = ttk.Treeview(window, columns=2)
table.grid(row=2, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("#1", text="Username")
table.bind("<Double-Button-1>", doubleClickTable) 

#Espacio
Label(window, text="Datos de Usuario", bg="black", fg="white", height=3).grid(row=3, column=0, columnspan=2)

#Usuario
Label(window, text="Usuario", bg="black", fg="white").grid(row=4,column=0)
usuario = Entry(window)
usuario.grid(row=4,column=1)

#Contraseña
Label(window, text="Password", bg="black", fg="white").grid(row=5,column=0)
clave = Entry(window)
clave.grid(row=5,column=1)

#Nombre
Label(window, text="Name", bg="black", fg="white").grid(row=6,column=0)
nombre = Entry(window)
nombre.grid(row=6,column=1)

#Apellido
Label(window, text="Last Name", bg="black", fg="white").grid(row=7,column=0)
apellido = Entry(window)
apellido.grid(row=7,column=1)

#Correo
Label(window, text="E-mail", bg="black", fg="white").grid(row=8,column=0)
correo = Entry(window)
correo.grid(row=8,column=1)

#Espacio
Label(window, bg="black", height=1).grid(row=9)

#Botón Insertar
insert = Button(window, text="Insertar Usuario", command=insertData, bg="black", fg="white")
insert.grid(row=10, columnspan=2)

#Espacio
Label(window, bg="black", height=1).grid(row=11)

#Botón Actualizar
update = Button(window, text="Actualizar Usuario", command=updateData, bg="black", fg="white")
update.grid(row=12, columnspan=2)
update["state"]="disabled"

#Espacio
Label(window, bg="black", height=1).grid(row=13)

#Botón Borrar
delete = Button(window, text="Borrar Usuario", command=deleteData, bg="black", fg="white")
delete.grid(row=14, columnspan=2)
delete["state"]="disabled"

#Espacio
Label(window, bg="black", height=1).grid(row=15)

#Buscar por Usuario
Label(window, text="Buscar Usuario", bg="black", fg="white").grid(row=16,column=0)
buscarUsuario = Entry(window)
buscarUsuario.grid(row=16,column=1)

#Correo
Label(window, text="Buscar E-mail", bg="black", fg="white").grid(row=17,column=0)
buscarCorreo = Entry(window)
buscarCorreo.grid(row=17,column=1)

#Espacio
Label(window, bg="black", height=1).grid(row=18)

#Botón Buscar
search = Button(window, text="Buscar", command=searchData, bg="black", fg="white")
search.grid(row=19, columnspan=2)
search["state"]="normal"

#Espacio
Label(window, bg="black", height=1).grid(row=20)

displayDocuments()
window.mainloop()
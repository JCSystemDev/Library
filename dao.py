from datetime import datetime

from pymongo import MongoClient


class DAO:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['biblioteca']

    def buscar(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.find_one(query)
        return result

    def crear(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def modificar(self, collection_name, query, new_values):
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': new_values})
        return result.modified_count

    def eliminar(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

    def mostrar(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.find(query)
        return list(result)

    def cerrar_conexion(self):
        self.client.close()

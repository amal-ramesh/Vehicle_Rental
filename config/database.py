from pymongo import MongoClient

client = MongoClient("mongodb+srv://amalrameshofficial01:Vehiclepassword@cluster0.qakr5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.vehicle_db

collection_name = db["vehicle_rental_collection"]
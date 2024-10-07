from fastapi import APIRouter, HTTPException
from models.vehicles import Vehicle
from config.database import collection_name
from schemas.schema import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/view")
async def view_vehicles():
    vehicle_list =list_serial(collection_name.find())
    return vehicle_list

@router.post("/add")
async def add_vehicle(vehicle:Vehicle):
    existing_vehicle = collection_name.find_one({"vehicle_number":vehicle.vehicle_number})
    if not existing_vehicle:
        collection_name.insert_one(dict(vehicle))
        return {f"{vehicle.vehicle_model} of number {vehicle.vehicle_number} added successfully"}
    else:
        return {f"Vehicle number {vehicle.vehicle_number} already exists !"}

@router.put("/rent/{id}")
async def rent_vehicle(id:str):
    rented_vehicle_list = list(collection_name.find({"rented":True},{"_id":True}))
    rented_id = []
    for rent_veh in rented_vehicle_list:
        rented_id.append(rent_veh["_id"])

    if ObjectId(id) not in rented_id:
        collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"rented": True}})
        return {"Rented vehicle with ID": id}
    else:
        return {"The vehicle is already rented !"}

@router.put("/return/{id}")
async def return_vehicle(id:str):
    rented_vehicle_list = list(collection_name.find({"rented":True},{"_id":True}))
    rented_id = []
    for rent_veh in rented_vehicle_list:
        rented_id.append(rent_veh["_id"])

    if ObjectId(id) in rented_id:
        collection_name.find_one_and_update({"_id":ObjectId(id)},{"$set" : {"rented":False}})
        return {"Returned vehicle with ID": id}
    else:
        return {"This vehicle is not yet rented !"}


@router.delete("/delete/{id}")
async def delete_vehicle(id:str):
    # existing_vehicle_list = list(collection_name.find({}, {"_id": True}))
    # existing_id = []
    # for exist_veh in existing_vehicle_list:
    #     existing_id.append(exist_veh["_id"])

    try:
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400 , detail="No such ID exists !")

    existing_vehicle_list = collection_name.find_one({"_id":obj_id})

    if existing_vehicle_list:
        collection_name.find_one_and_delete({"_id":ObjectId(id)})
        return {"Deleted vehicle with ID": id}
    else:
        return {"No such vehicle to delete !"}


@router.get("/rented_list")
async def view_rented_vehicle():
    rented_vehicle_list = list_serial(collection_name.find({"rented":True}))
    return rented_vehicle_list

@router.get("/available_list")
async def view_availabe_vehicles_for_rent():
    available_vehicle_list = list_serial(collection_name.find({"rented":False}))
    return available_vehicle_list

@router.get("/total_price")
async def cal_tot_price_of_rented_vehicle():
    rented_vehicles = list(collection_name.find({"rented": True}, {"price": True}))
    total_price = sum(rent_veh["price"] for rent_veh in rented_vehicles)
    return {"Total price of rented vehicles ": total_price}


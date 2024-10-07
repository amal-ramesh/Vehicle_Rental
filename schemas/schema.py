def individual_serializer(vehicle) -> dict:
    return {
        "id" : str(vehicle["_id"]),
        "Vehicle model" : str(vehicle["vehicle_model"]),
        "Vehicle company" : str(vehicle["vehicle_company"]),
        "Vehicle number" : int(vehicle["vehicle_number"]),
        "Rented" : bool(vehicle["rented"]),
        "Price" : float(vehicle["price"])

    }

def list_serial(vehicles) -> list:
    return [individual_serializer(vehicle) for vehicle in vehicles]
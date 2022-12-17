from bson import ObjectId


def generate_unique_object_id():
    return str(ObjectId())
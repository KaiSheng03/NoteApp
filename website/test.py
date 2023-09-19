from bson import ObjectId

class Id():
    def __init__(self, id):
        self.id = id


a = Id(ObjectId())

print(type(str(a.id)))

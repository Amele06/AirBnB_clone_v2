class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def delete(self, obj=None):
        """deletes obj from ___objects if it's inside"""
        if obj is not None:
            key = obj.__class__.name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
            self.save()

    def all(self, cls=None):
        """Returns the list of objects of one type of class"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.item():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
                return new_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            json.dump({key: val.to_dict()
                      for key, val in self.__objects.items()}, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)
                self.__objects = {}
                for key, val in data.items():
                    cls_name = val['__class__']
                    self.__objects[key] = classes[cls_name](**val)
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

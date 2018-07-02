"""
This module will act as a persistent storage for its child class.

Persistent storage can be designed in 2 ways:
    - The overall storage is managed by multiple client and they have
      control over some part of total storage. They manage the memory based
      on some predefined policies.
    - Overall storage is managed by single entity and it handles all the storage
      and defines the policy of storing and removing the data based on its usage.

In case of Multiple clients managing the storage, they have to be assigned a fixed
beforehand. This kills some level of dynamism.

In case of Single client, the objects that are haven't been used for quite some time
can be removed completely thus providing more space to frequently objects which is
not possible for multiple client architecture.


I am constructing a multiple client, besides some of its demerits, just to understand
how to construct it. Some changes can be made later to make it Single client system and
restore all the features. These changes will include introduction of a (singleton) class
in between pymongo and StorageManager
"""


# from pymongo import MongoClient
# client = MongoClient()
# database = client['telegram_bot']

# class UsageManager:
#     def __init__(self):
#         self.usage_queue =


class StorageManager:
    def __init__(self, name):
        """ Call this function after defining all the variables in __init__ with `self.` notation """
        self.name = name
        self.usage_queue = list()

    def store(self):
        # TODO: store all the variables in persistence database
        pass

    def get(self, name):
        """ Prefer the usage over `self.name` notation as the `name` might have been evicted/removed from the memory"""
        # TODO: include the check if this attribute is in memory or not
        return self.__dict__.get(name, None)

    def upsert(self, name, value, insert=False):
        if insert or name in self.__dict__:
            self.__dict__[name] = value
            return value
        raise AttributeError("No attribute named `{}`".format(name))

    def insert(self, name, value):
        """ for defining a class variable """
        self.upsert(name, value, True)

    def update(self, name, value):
        """ For updating a class variable.
        This will assign the variable `name` with `value`.
        If you are looking to new values to a list, try append function"""
        self.upsert(name, value, False)

    def append(self, name, mutable_values):
        """ Use of appending data to mutable data structures """
        mutable = self.__dict__.get(name, None)
        if mutable is not None:
            mutable += mutable_values
        else:
            self.__dict__[name] = mutable_values

    # def add(self, key, ):
    # TODO: divide all the operations in the categories of
    # insert, update, upsert for normal variables, mutables and dicts

    def delete(self, name):
        """ To deallocate a class variable """
        if name in self.__dict__:
            value = self.__dict__[name]
            del self.__dict__[name]
            return value
        return None

    def evict(self):
        # just like cache eviction
        # release the memory for new files/data to be written in memory
        # Define some eviction policy
        pass

# class Child(StorageManager):
#     def __init__(self, name):
#         self.blah = "blah"
#         super().__init__(name)
#
# # test = Child("blah_Blah")
# # # print(test.get())
# # print(test.update('ho', "hioasoopiwefqweefqwefzzzzzzzzzzzzzzzzzzzz", True))
# # print(test.delete('ho'))
# # print(test.delete('ho'))

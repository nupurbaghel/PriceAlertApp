import uuid
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors
from src.common.database import Database

__author__ = "Nupur Baghel"
class Store(object):
    def __init__(self,name,url_prefix,tag_name,query,_id=None):
        self.name=name
        self.url_prefix=url_prefix
        self.tag_name=tag_name
        self.query=query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {} >".format(self.name)

    @classmethod
    def get_by_id(cls,_id):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{'_id':_id}))

    def json(self):
        return {
            '_id':self._id,
            'name':self.name,
            'url_prefix':self.url_prefix,
            'tag_name':self.tag_name,
            'query':self.query
        }

    @classmethod
    def get_by_name(cls,store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{'name':store_name}))

    @classmethod
    def get_by_url_prefix(cls,url_prefix):
        try:
            return cls(**Database.find_one(StoreConstants.COLLECTION,{'url_prefix':{"$regex":'^{}'.format(url_prefix)}}))
        except:
            pass

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION,{'_id':self._id},self.json())

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION,{})]

    @classmethod
    def find_by_url(cls,url):

        for i in range(0,len(url)+1):
            #try:
                length=len(url)
                store=cls.get_by_url_prefix(url[:length-i+1])
                if store is not None:
                    return store
            #except:
        raise StoreErrors.StoreNotFoundException("The URL prefix used to find the store was not found.")

    def delete(self):
        Database.remove(StoreConstants.COLLECTION,{'_id':self._id})
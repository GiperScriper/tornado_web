import pymongo
import json

from bson.json_util import dumps
from bson.objectid import ObjectId

DB = pymongo.Connection("localhost", 27017)['notes']
coll = DB['notes']


def get_note_or_notes(_id):
    """Returns all notes or one note
    """
    result = []
    
    if _id:
        note = coll.find_one({"_id": ObjectId(_id)})
        result = dumps(note, indent=4)
    else:
        notes = coll.find()                
        result = dumps(notes, indent=4)

    return result
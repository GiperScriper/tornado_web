import pymongo
import json
import time

from bson.json_util import dumps
from bson.objectid import ObjectId

# connect to Notes database
db = pymongo.Connection("localhost", 27017)['notes']


def get_note_or_notes(_id, method):
    """Returns all notes or one note
    """
    result = []
    status_code = 200
    
    if _id:
        note = db.notes.find_one({"_id": ObjectId(_id)})
        if note:
            result = dumps(note, indent=4)
        else:
            result = {'message': 'Sorry, note with this id not found :('}
            status_code = 404

    else:
        notes = list(db.notes.find())
        data = {'count': len(notes), 'method': method, 'data': notes}                
        result = dumps(data, indent=4)

    return (result, status_code)


def delete_note(_id):
    """Delete note
    """
    result = []
    status_code = 204
    
    if _id:
        note = db.notes.find_one({"_id": ObjectId(_id)})
        if note:
            db.notes.remove({"_id": ObjectId(_id)})
        else:
            result = {'message': 'Sorry, note with this id not found :('}
            status_code = 404

    return (result, status_code)


def create_note(data):
    """Save note
    """
    notes_fields = ['title', 'body', 'author', 'tags']
    
    result = { key: (data[key] if key in data.keys() else None) for key in notes_fields }
    result['date_added'] = int(time.time())

    db.notes.insert(result)    
    status_code = 201
    
    return (dumps(result), status_code)    




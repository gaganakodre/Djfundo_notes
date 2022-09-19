import json
import logging

from .task import Redis

logging.basicConfig(filename='Djfundo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class RedisNote:
    """
    Class is used to perform curd operation with the redis
    """

    def __init__(self):
        self.redis = Redis()

    def save(self, notes, user_id):
        note_dict = self.get(user_id)
        note_id = notes.get('id')
        note_dict.update({note_id: notes})
        self.redis.setter(user_id, json.dumps(note_dict))

    def get(self, user_id):
        payload = self.redis.getter(user_id)
        return json.loads(payload) if payload else {}

    # def update(self, notes, user_id):
    #     note_id = str(notes.get('id'))
    #     notes_dict = self.get(user_id)
    #     note = notes_dict.get(note_id)
    #     if note is not None:
    #         notes_dict.update({note_id: notes})
    #         self.redis.setter(user_id, json.dumps(notes_dict))

    def delete(self, user_id, note_id):
        notes_dict = self.get(user_id)
        note = notes_dict.get(str(note_id))
        if note is not None:
            notes_dict.pop(str(note_id))
            self.redis.setter(user_id, json.dumps(notes_dict))

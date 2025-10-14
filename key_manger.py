from random import shuffle
from math import ceil


class KeyManger:
    def __init__(self, keys):
        self.keys = keys
        shuffle(self.keys)
        self.keys_index = -1

    def split(self, no_of_chunks):
        key_mangers = []
        chunk_size = ceil(len(self.keys) / no_of_chunks)
        for i in range(0, len(self.keys), chunk_size):
            km = KeyManger(self.keys[i : i + chunk_size])
            key_mangers.append(km)
        return key_mangers

    def get_key(self):
        self.keys_index = (self.keys_index + 1) % len(self.keys)
        return self.keys[self.keys_index]

    def delete_key(self):
        del self.keys[self.keys_index]
        if len(self.keys) == 0:
            print("all keys are used")
            return 1

        elif self.keys_index == 0:
            self.keys_index = -1

        elif self.keys_index == len(self.keys):
            self.keys_index = -1

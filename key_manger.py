from random import shuffle


class KeyManger:
    def __init__(self, keys_string):
        self.keys = keys_string.split(",")
        shuffle(self.keys)
        self.keys_index = -1

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

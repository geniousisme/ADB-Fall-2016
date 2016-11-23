class WrongRangeError(Exception):
   	def __init__(self):
   		self.message = "range must be 0 - 1 !"

class KeyMustBeSetError(Exception):
    def __init__(self):
        self.message = "The key must be set object!"

class CantAppendError(Exception):
    def __init__(self):
        self.message = "The key already exist!"
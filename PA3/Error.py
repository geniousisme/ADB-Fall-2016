class WrongRangeError(Exception):
   	def __init__(self):
   		self.message = "WrongRangeError: range must be 0 - 1 !"

class KeyMustBeSetError(Exception):
    def __init__(self):
        self.message = "KeyMustBeSetError: The key must be set object!"

class CantAppendError(Exception):
    def __init__(self):
        self.message = "CantAppendError: The key already exist!"
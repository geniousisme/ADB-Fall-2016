from collections import OrderedDict

SETITEM = "setitem"
GETITEM = "getitem"
DELITEM = "delitem"
GET = "get"

class KeyMustBeSetError(Exception):
    def __init__(self):
        self.message = "The key must be set object!"

class ItemSet(object):
    def __init__(self, set=set(), supp=0.0):
        self.set = set
        self.supp = supp

    def __eq__(self, other):
        return self.set == other.set 

    def __repr__(self):
        return "<ItemSet: " + str(self.set) + ">"

    def __str__(self):
        return  "itemSet: " + str(self.set) 

class Candidate(object):
    def __init__(self):
        self.candidates = OrderedDict()

    def __iter__(self):
        return iter(self.candidates)
    
    def __repr__(self):
        return "<Candidate: " + str(self.candidates) + ">"

    def __str__(self):
        return "Candidate: " + str(self.candidates)

    def __setitem__(self, key, val):
        try:
            if not isinstance(key, set):
                raise KeyMustBeSetError
            self.candidates[str(key)] = val

        except KeyMustBeSetError as e:
            print e.message

    def __getitem__(self, key):
        try:
            if not isinstance(key, set):
                raise KeyMustBeSetError
            return self.candidates[str(key)]

        except KeyMustBeSetError as e:
            print e.message

    def __delitem__(self, key):
        try:
            if not isinstance(key, set):
                raise KeyMustBeSetError
            del self.candidates[str(key)]

        except KeyMustBeSetError as e:
            print e.message

    def get(self, key, default=0):
        try:
            return self.candidates[str(key)]

        except KeyMustBeSetError as e:
            print e.message

        except KeyError as e:
            self.candidates[str(key)] = default
            return default

    def get_itemset(self, key):
        try:
            if not isinstance(key, set):
                raise KeyMustBeSetError
            supp = self.candidates[str(key)]
            item_set = ItemSet(key, supp)
            return item_set

        except KeyMustBeSetError as e:
            print e.message

    def method_interface(self, method_name, key, val=0.0):
        try:
            if not isinstance(key, set):
                raise KeyMustBeSetError

            if method_name == SETITEM:
                self.candidates[str(key)] = val

            elif method_name == GETITEM:
                return self.candidates[str(key)]

            elif method_name == DELITEM:
                del self.candidates[str(key)]

            elif method_name == GET:
                return self.candidates[str(key)]                

        except KeyMustBeSetError as e:
            print e.message

        except KeyError as e:
            if method_name == GET:
                self.candidates[str(key)] = default
                return default
            else:
                print e.message



    def append_itemset(itemset):
        self.candidates[str(itemset.set)] = itemset.supp

if __name__ == "__main__":
    from Candidate import ItemSet, Candidate
    ct = Candidate()
    ct[set([1, 2, 3])] = 1


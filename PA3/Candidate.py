from collections import OrderedDict

SETITEM = "setitem"
GETITEM = "getitem"
DELITEM = "delitem"
GET = "get"
APPEND = "append"


class KeyMustBeSetError(Exception):
    def __init__(self):
        self.message = "The key must be set object!"

class CantAppendError(Exception):
    def __init__(self):
        self.message = "The key already exist!"

class ItemSet(object):
    def __init__(self, val=set()):
        if not isinstance(val, set):
            if not isinstance(val, list):
                val = [val]
            val = set(val)
        self.val = val

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.val == set(other)

        if isinstance(other, set):
            return self.val == other

        return self.val == other.val

    def __repr__(self):
        return "<ItemSet: " + str(self.val) + ">"

    def __str__(self):
        return  "itemSet: " + str(self.val)

    def __hash__(self):
        return hash(tuple(sorted(self.val)))

    def __len__(self):
        return len(self.val)

    def __getitem__(self, key):
        return tuple(sorted(self.val))[key]

    def __index__(self):
        return tuple(sorted(self.val))

class Candidate(object):
    def __init__(self, key=None, val=0.0):
        self.candidates = OrderedDict()

    def __len__(self):
        return len(self.candidates)

    def __nonzero__(self):
        return len(self.candidates) != 0

    def __iter__(self):
        return iter(self.candidates)
    
    def __repr__(self):
        return "<Candidate: " + str(self.candidates) + ">"

    def __str__(self):
        return "Candidate: " + str(self.candidates)

    def __setitem__(self, key, val):
        self.method_interface(SETITEM, key, val)

    def __getitem__(self, key):
        return self.method_interface(GETITEM, key)

    def __delitem__(self, key):
        self.method_interface(DELITEM, key)

    def get(self, key, default=0):
        return self.method_interface(GET, key, default)

    def append(self, key):
        self.method_interface(APPEND, key)
        # self.candidates[str(itemset.set)] = itemset.supp

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
            if not isinstance(key, ItemSet):
                key = ItemSet(key)

            if method_name == SETITEM:
                self.candidates[key] = val

            elif method_name == GETITEM:
                return self.candidates[key]

            elif method_name == DELITEM:
                del self.candidates[key]

            elif method_name == GET:
                return self.candidates[key]

            elif method_name == APPEND:
                if self.candidates.get(key) is None:
                    self.candidates[key] = val
                else:
                    raise CantAppendError

        except KeyMustBeSetError as e:
            print e.message

        except CantAppendError as e:
            print e.message

        except KeyError as e:
            if method_name == GET:
                self.candidates[key] = val
                return val
            else:
                print e

if __name__ == "__main__":
    from Candidate import ItemSet, Candidate
    ct = Candidate()
    it1 = ItemSet(1)
    ct[it1] = 1
    ct[ItemSet(1)] = 2
    ct[set([1, 2, 3])] = 1
    print ct.get(set([1,2]))


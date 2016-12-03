import sys

from collections import OrderedDict

from Error import KeyMustBeSetError, CantAppendError

SETITEM = "setitem"
GETITEM = "getitem"
DELITEM = "delitem"
GET = "get"
APPEND = "append"
EXTEND = "extend"

class ItemSet(object):
    def __init__(self, itm_set=tuple(), supp=0.0, conf=0.0):
        if not isinstance(itm_set, tuple):
            if not isinstance(itm_set, set):
                if not isinstance(itm_set, list):
                    itm_set = [itm_set]
                itm_set = set(itm_set)
        itm_set = tuple(sorted(itm_set))
        self.itm_set = itm_set
        self.supp = supp
        self.conf = conf

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.itm_set == other

        if isinstance(other, set):
            return self.itm_set == tuple(other)

        if isinstance(other, list):
            return self.itm_set == tuple(other)

        return self.itm_set == other.itm_set

    def __repr__(self):
        return "<ItemSet: " + str(self.itm_set) + ">"

    def __str__(self):
        return  "itemSet: " + str(self.itm_set)

    def __hash__(self):
        return hash(self.itm_set)

    def __len__(self):
        return len(self.itm_set)

    def __getitem__(self, key):
        return self.itm_set[key]

    def __iter__(self):
        return iter(self.itm_set)

    def __index__(self):
        return self.itm_set

    def is_subset_of(self, target):
        if not isinstance(target, set):
            target = set(target)
        return set(self).issubset(target)

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

    def extend(self, key):
        self.method_interface(EXTEND, key)

    def method_interface(self, method_name, key, val=0.0):
        try:
            if not (isinstance(key, ItemSet) or isinstance(key, Candidate)):
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

            elif method_name == EXTEND:
                if not isinstance(key, Candidate):
                    raise CantAppendError
                candidate = key
                for itemset in candidate:
                    self.method_interface(APPEND, itemset, candidate[itemset])

        except KeyMustBeSetError as e:
            print e.message
            sys.exit(1)

        except CantAppendError as e:
            print e.message
            sys.exit(1)

        except KeyError as e:
            if method_name != GET:
                raise KeyError
                sys.exit(1)

            self.candidates[key] = val
            return val

if __name__ == "__main__":
    from Candidate import ItemSet, Candidate
    ct = Candidate()
    it1 = ItemSet(1)
    ct[it1] = 1
    ct[ItemSet(1)] = 2
    ct[set([1, 2, 3])] = 1
    print ct.get(set([1, 2]))


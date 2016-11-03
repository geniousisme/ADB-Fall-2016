from enum import Enum

class WrongRangeError(Exception):
   def __init__(self):
    self.message = ""

class Web(Enum):
    DOC = -4
    XDOC = -5
    Url = "Url"
    Title = "Title"
    Desc = "Description"
    References = "\nReferences\n"

def extract_query_for_category(category_name):
    f = open(category_name + '.txt', 'r')
    category_query_dict = {}
    for line in f:
        line = line.replace('\n', '')
        category_and_queries = line.split(' ')
        category = category_and_queries[0]
        query = ' '.join(category_and_queries[1:])
        if category_query_dict.get(category):
            category_query_dict[category].append(query)
        else:
            category_query_dict[category] = [query]
    f.close()
    return category_query_dict


if __name__ == "__main__":
    print extract_query_for_category("Root")
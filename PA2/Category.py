from enum import Enum

from Util import extract_query_for_category

class CategName(Enum):
    Root = "Root"
    Health = "Health"
    Sports = "Sports"
    Computers = "Computers"

class Category(object):
    def __init__(self, categ_name):
        self.name = categ_name
        self.sub_categs = []
        self.queries = []

    def __str__(self):
        return "Category: " + self.name

    def __repr__(self):
        return "Category: " + self.name

def build_category(source_categ):
    categ_query_dict = extract_query_for_category(source_categ.name)
    for categ_name, queries in categ_query_dict.items():
        new_categ = Category(categ_name)
        new_categ.queries = categ_query_dict[categ_name]
        source_categ.sub_categs.append(new_categ)

def init_categories():
    root_categ = Category(CategName.Root)
    build_category(root_categ)
    for categ in root_categ.sub_categs:
        build_category(categ)
    # for sub_categ in root_categ.sub_categs:
    #     print sub_categ
    #     print sub_categ.queries
    #     print sub_categ.sub_categs
    #     for sub_sub_categ in sub_categ.sub_categs:
    #         print "\t", sub_sub_categ
    #         print "\t", sub_sub_categ.queries
    return root_categ

if __name__ == "__main__":
    init_categories()

    




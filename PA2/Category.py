from Util import extract_query_for_category

Root = "Root"

class Category(object):
    def __init__(self, categ_name):
        self.name = categ_name
        self.parent_categ = None
        self.sub_categs = []
        self.queries = []

    def __str__(self):
        return "Category: " + self.name

    def __repr__(self):
        return "<Category_Obj: " + self.name + ">"

    def __eq__(self, other):
        return self.name == other.name

    def get_sub_categ(self, target_categ):
        for sub_categ in self.sub_categs:
            if target_categ.name == sub_categ.name:
                return sub_categ
        return None

    def is_root_categ(self):
        return self.name == Root

    def show(self):
        print self
        for sub_categ in self.sub_categs:
            print "\t", sub_categ
            print "\t", sub_categ.queries
            print "\t", sub_categ.sub_categs
            for sub_sub_categ in sub_categ.sub_categs:
                print "\t\t", sub_sub_categ
                print "\t\t", sub_sub_categ.queries
                print "\t\t", sub_sub_categ.sub_categs

    def show_classif(self):
        print "\n\nClassification:"
        classif_str = self.name
        for sub_categ in self.sub_categs:
            if not sub_categ.sub_categs:
                print classif_str + '/' + sub_categ.name
            else:
                classif_str += '/' + sub_categ.name
                for sub_sub_categ in sub_categ.sub_categs:
                    print classif_str + '/' + sub_sub_categ.name
        print "\n\n"
                
def build_category(source_categ):
    categ_query_dict = extract_query_for_category(source_categ.name)
    for categ_name, queries in categ_query_dict.items():
        new_categ = Category(categ_name)
        new_categ.parent_categ = source_categ
        new_categ.queries = categ_query_dict[categ_name]
        source_categ.sub_categs.append(new_categ)

def init_categories():
    root_categ = Category(Root)
    build_category(root_categ)
    for categ in root_categ.sub_categs:
        build_category(categ)
    return root_categ

if __name__ == "__main__":
    init_categories()

    




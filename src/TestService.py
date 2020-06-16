
# Returns a list of class names read from `file_name`
def load_class_names(file_name):
    with open(file_name, 'r') as f:
        class_names = f.read().splitlines()
    return class_names

_CLASS_NAMES_FILE = 'coco.names'
load_class_names(_CLASS_NAMES_FILE)
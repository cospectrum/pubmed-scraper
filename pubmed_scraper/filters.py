
def filter_authors(tag) -> bool:
    class_attr = 'full-authors'
    if tag.name == 'span' and class_attr in tag.get('class', {}):
        return True
    return False


def filter_cite(tag) -> bool:
    if tag.name != 'span':
        return False
    class_attr_1 = 'docsum-journal-citation'
    class_attr_2 = 'full-journal-citation'
    if class_attr_1 in tag.get('class', {}) or class_attr_2 in tag.get('class', {}):
        return True
    return False


def filter_linkout_category(tag) -> bool:
    class_attr = 'linkout-category'
    if class_attr in tag.get('class', {}):
        return True
    return False


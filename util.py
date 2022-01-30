# coding utf-8

def confirm_smaller_length(list1, list2):
    if len(list1) < len(list2):
        return len(list1)

    return len(list2)

def confirm_bigger_length(list1, list2):
    if len(list1) > len(list2):
        return len(list1)

    return len(list2)



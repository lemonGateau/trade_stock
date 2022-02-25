import pandas as pd

def confirm_smaller_length(list1, list2):
    if len(list1) < len(list2):
        return len(list1)

    return len(list2)

def confirm_bigger_length(list1, list2):
    if len(list1) > len(list2):
        return len(list1)

    return len(list2)

def generate_constant_df(values, keys, length):
    data = {}

    for i, value in enumerate(values):
        data[keys[i]] = [value] * length

    return pd.DataFrame(data=data, columns=keys)

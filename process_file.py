import sys
sys.path.append('..')
import json
import csv
from collections import OrderedDict


# ~~~~~~~~~~      jsonファイル操作      ~~~~~~~~~~
# 書き込み(上書き)
def json_write(dic, path):
    with open(path, 'w') as f:
        json.dump(dic, f, indent=4)

# 読み込み
def json_read(path):
    with open(path, 'r') as f:
        dic = json.load(f)
        return dic

# 書き込み(追記)
def json_add(word, path):
    with open(path, 'a') as f:
        json.dump(word, f, indent=4)


# ~~~~~~~~~~      csvファイル操作      ~~~~~~~~~~
# 書き込み(ファイルが存在しなければ新規作成)
def csv_write(word, path):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(word)

# 複数行書き込み(ファイルが存在しなければ新規作成)
def csv_writes(words, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(words)

# 読み込み
def csv_read(path):
    with open(path, 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        reader = [row for row in reader]    # 2次元配列化
        return reader

# 追記(ファイルが存在しなければ新規作成)
def csv_add(word, path):
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(word)

# 複数行追記(ファイルが存在しなければ新規作成)
def csv_adds(words, path):
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(words)

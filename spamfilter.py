import os
import re
from collections import Counter
import pprint as pp


class Spamfilter():
    """spam filter class which will accept training directory"""

    def __init__(self, training_dir):
        self.ham_table = dict(Counter(find_frequency(training_dir + "ham/")))
        self.spam_table = dict(Counter(find_frequency(training_dir + 'spam/')))
        self.uniq_h_toks = len(self.ham_table)
        self.uniq_s_toks = len(self.spam_table)
        self.total_h_toks = sum(self.ham_table.values())
        self.total_s_toks = sum(self.spam_table.values())
        self.tok_arr = sorted(list(self.ham_table.keys()) + list(self.spam_table.keys()))
        self.frequency_table = self.create_frequency_table()

    # def create_frequency_table(self):
    #     freq_table = {}
    #     for tok in self.tok_arr:
    #         print(tok)
    #         table_entry = []
    #         spam_freq = self.spam_table.get(tok, 0)
    #         table_entry.append(('spam_freq', spam_freq))
    #         ham_freq = self.ham_table.get(tok, 0)
    #         table_entry.append(('ham_freq', ham_freq))
    #         prob_spam = (spam_freq + 1 / float(self.uniq_s_toks)) / (self.total_s_toks + 1)
    #         table_entry.append(('prob_spam', prob_spam))
    #         prob_ham = (ham_freq + 1 / float(self.uniq_h_toks)) / (self.total_h_toks + 1)
    #         table_entry.append(('prob_ham', prob_ham))
    #         freq_table[tok] = table_entry
    #     return freq_table

    def create_frequency_table(self):
        freq_table = {}
        for tok in self.tok_arr:
            print(tok)
            table_entry = {}
            spam_freq = self.spam_table.get(tok, 0)
            table_entry['spam_freq'] = spam_freq
            ham_freq = self.ham_table.get(tok, 0)
            table_entry['ham_freq'] = ham_freq
            prob_spam = (spam_freq + 1 / float(self.uniq_s_toks)) / (self.total_s_toks + 1)
            table_entry['prob_spam'] = prob_spam
            prob_ham = (ham_freq + 1 / float(self.uniq_h_toks)) / (self.total_h_toks + 1)
            table_entry['prob_ham'] = prob_ham
            freq_table[tok] = table_entry
        return freq_table


def tokens(str, tok_size=3):
    return [str[i:i+tok_size] for i in range(len(str) - tok_size + 1)]


def clean_split(string):
    return re.sub(r'[^\s\w]|_', '', string).lower().split()


def file_tokens(filepath):
    toks = []
    try:
        with open(filepath, encoding="utf8", errors='ignore') as fp:
            for line in fp:
                words = clean_split(line)
                toks.extend(words)
    except FileNotFoundError as e:
        print("Error:" + str(e))
    return [x for x in toks if len(x) < 10]


def find_frequency(dir_name):
    big_list = []
    filenames = os.listdir(dir_name)  # array of filenames in directory
    # print(filenames)
    for f in filenames:
        big_list.extend(file_tokens(dir_name + f))
    return big_list





# count = dict(file_tokens('test2'))
# pp.pprint(count)
# print(os.listdir('./emails/training/ham/5467435763'))
# pp.pprint(file_tokens(find_frequency('./small/')))

# dir_name = 'emails/training/ham/'
# list = find_frequency(dir_name)
# print(list)
# count = dict(Counter(list))
# pp.pprint(count)
# print(len(os.listdir(dir_name)))


filter = Spamfilter('emails/training/')
# pp.pprint(filter.ham_table)
# print("\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^")
# pp.pprint(filter.spam_table)
#
# print(filter.total_h_toks)
# print(filter.total_s_toks)
# print(filter.uniq_h_toks)
# print(filter.uniq_s_toks)
# pp.pprint(filter.tok_arr)

filter.create_frequency_table()
pp.pprint(filter.frequency_table)

import os
import re
from collections import Counter
import pprint as pp
import math


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
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        self.spam_list = []
        self.ham_list = []

    def create_frequency_table(self):
        freq_table = {}
        for tok in self.tok_arr:
            print(tok)
            entry = {}
            s_freq = self.spam_table.get(tok, 0)
            entry['spam_freq'] = s_freq
            h_freq = self.ham_table.get(tok, 0)
            entry['ham_freq'] = h_freq
            s_prob = (s_freq + 1 / float(self.uniq_s_toks)) / (self.total_s_toks + 1)
            entry['prob_spam'] = s_prob
            h_prob = (h_freq + 1 / float(self.uniq_h_toks)) / (self.total_h_toks + 1)
            entry['prob_ham'] = h_prob
            freq_table[tok] = entry
        return freq_table

    def get_prob_spam(self, token):
        val = self.frequency_table.get(token)
        if val is not None:
            return val['prob_spam']
        else:
            return (1.0 / self.uniq_s_toks) / (self.total_s_toks + 1)

    def get_prob_ham(self, token):
        val = self.frequency_table.get(token)
        if val is not None:
            return val['prob_ham']
        else:
            return (1.0 / self.uniq_h_toks) / (self.total_h_toks + 1)

# todo jsut pass in a lsit of tokens, instead of doing
    #  it twice for each spam and ham
    def prob_msg_spam(self, filepath):
        tokens = file_tokens(filepath)
        sm = 0
        for tok in tokens:
            sm += math.log10(self.get_prob_spam(tok))
        return sm

    def prob_msg_ham(self, filepath):
        tokens = file_tokens(filepath)
        sm = 0
        for tok in tokens:
            sm += math.log10(self.get_prob_ham(tok))
        return sm

    def classify(self, filepath):
        self.file_count += 1
        if self.prob_msg_spam(filepath) > self.prob_msg_ham(filepath):
            self.count_spam += 1
            self.spam_list.append(filepath)
            return True
        else:
            self.count_ham += 1
            self.ham_list.append(filepath)
            return False


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
print(filter.get_prob_ham('zones'))
print(filter.get_prob_spam('zones'))

print(filter.classify('emails/training/spam/01358.eb6c715f631ee3d22b135adb4dc4e67d'))

import os
import re
from collections import Counter
import pprint as pp
import math


class Spamfilter():
    """spam filter class which will accept training directory"""

    def __init__(self, training_dir):
        print('Training filter with known ham...')
        self.ham_table = dict(Counter(find_frequency(training_dir + "ham/")))
        print('Training filter with known spam...')
        self.spam_table = dict(Counter(find_frequency(training_dir + 'spam/')))
        self.uniq_h_toks = len(self.ham_table)
        self.uniq_s_toks = len(self.spam_table)
        self.total_h_toks = sum(self.ham_table.values())
        self.total_s_toks = sum(self.spam_table.values())
        self.tok_arr = sorted(list(self.ham_table.keys()) + list(self.spam_table.keys()))
        self.freq_tab = self.create_frequency_table()
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        self.spam_list = []
        self.ham_list = []

    def create_frequency_table(self):
        freq_table = {}
        for tok in self.tok_arr:
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
        val = self.freq_tab.get(token)
        if val is not None:
            return val['prob_spam']
        else:
            return (1.0 / self.uniq_s_toks) / (self.total_s_toks + 1)

    def get_prob_ham(self, token):
        val = self.freq_tab.get(token)
        if val is not None:
            return val['prob_ham']
        else:
            return (1.0 / self.uniq_h_toks) / (self.total_h_toks + 1)

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

    def classify_all(self, dir_path, known_type):
        self.ham_list = []
        self.spam_list = []
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        print("\nClassifying all emails found in directory: " + dir_path)
        filenames = os.listdir(dir_path)
        for f in filenames:
            self.classify(dir_path + f)

        if known_type == 'spam':
            correct = self.count_spam/float(self.file_count)
        else:
            correct = self.count_ham/float(self.file_count)

        print('Total spam: \t' + str(self.count_spam))
        print('Total ham:  \t' + str(self.count_ham))
        print("Percentage correctly classified: " + str(correct*100))

    def clean_table(self, min_freq):
        rm_keys = []
        for k, v in self.freq_tab.items():
            if (v['spam_freq'] + v['ham_freq'] < min_freq or
                    0.45 < (v['prob_spam'] / (v['prob_spam'] + v['prob_ham'])) < 0.55):
                rm_keys.append(k)
        for k in rm_keys:
            print("deleting " + str(k) + " from freq table in clean()")
            del self.freq_tab[k]

    def print_table_info(self):
        print('\n\n=================================')
        print('TRAINING AND FREQUENCY TABLE INFO')
        print("=================================")
        print('Total unique tokens in all spam messages:' + str(len(self.spam_table)))
        print('Total unique tokens in all ham messages:' + str(len(self.ham_table)))
        print('Total unique tokens in all combined messages:' + str(len(self.freq_tab)))
        print('Total number of spam mails: ' + str(len(os.listdir('emails/testing/spam/'))))
        print('Total number of ham mails: ' + str(len(os.listdir('emails/testing/ham/'))))




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
    filenames = os.listdir(dir_name)
    for f in filenames:
        big_list.extend(file_tokens(dir_name + f))
    return big_list


spam_filter = Spamfilter('emails/training/')
spam_filter.print_table_info()
spam_filter.classify_all("emails/testing/spam/", 'spam')
spam_filter.classify_all("emails/testing/ham/", 'ham')


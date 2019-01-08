import spamfilter as sf

filter = sf.Spamfilter('emails/training/')
filter.print_table_info()
filter.classify_all("emails/testing/spam/", 'spam')
filter.classify_all("emails/testing/ham/", 'ham')
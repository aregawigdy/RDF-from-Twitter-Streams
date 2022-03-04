
import nltk.tokenize as nt
import nltk
text="Being more Pythonic is good for health."
ss = nt.sent_tokenize(text)
tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent]
pos_sentences[[('Being', 'VBG'), ('more', 'JJR'), ('Pythonic', 'NNP'), ('is', 'VBZ'), ('good', 'JJ'), ('for', 'IN'), ('health', 'NN'), ('.', '.')]]
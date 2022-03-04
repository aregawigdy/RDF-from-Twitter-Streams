
import tagme
import time
import json
import functools

tagme.GCUBE_TOKEN = "93eb5238-bf49-4293-84e8-302dcf40944b-843339462"
# nlp = spacy.load("en_core_web_sm")

@functools.lru_cache(maxsize=None)
def mentions_func(tweet):
    entity_mentions = tagme.mentions(tweet)
    return entity_mentions


text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19 3rd wave - Sign the Petition!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19 3rd wave - Sign the Petition!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19 3rd wave - Sign the Petition!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19 3rd wave - Sign the Petition!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
text = "IIT KGP: Postpone GATE2022 exam date due to COVID-19!"
start_time = time.time()
result = mentions_func(text)
for mention in result.mentions:
    if mention.linkprob > 0.01:
        print(mention.mention + " lp=" + str(mention.linkprob))
print("--- %s seconds ---" % (time.time() - start_time))
print(mentions_func.cache_info())

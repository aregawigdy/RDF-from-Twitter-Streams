
import re
import string

import tweepy
from spacy.util import minibatch, compounding
import random
import json
from spacy.lang.en import English
from tweepy import OAuthHandler, Stream, StreamListener
from gensim.parsing.preprocessing import remove_stopwords
import spacy
import tagme
# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = "93eb5238-bf49-4293-84e8-302dcf40944b-843339462"

nlp = spacy.load("en_core_web_sm")

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "yzw16SfR4rnfZb4m2JnzRryPr"
consumer_secret = "88OAWEkNfLdSzRplcbI2PQmn0vjSl1AVi5KhRIFMVSiEDfsm9p"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1178352707821658113-xXcRH018zjZX3RfxwH38FEPIjNJIHU"
access_token_secret = "oZvFOW47k13tKWHONSIa7GwIENCu6mbHMb3iMrE3o5QIH"


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        # Import and load the spacy model
        # Getting the ner component
        # ner = nlp.get_pipe('ner')
        # New label to add
        """LABEL = "DISEASE"
        # Training examples in the required format
        TRAIN_DATA = [("Diphtheria is an infection caused by the bacterium Corynebacterium diphtheriae.", {"entities": [(0, 10, "DISEASE")]}),
                      ("HIV/AIDS is a virus that damages the immune system.", {"entities": [(0, 8, "DISEASE")]}),
                      ("Influenza is an infectious disease caused by an influenza virus.", {"entities": [(0, 9, "DISEASE")]}),
                      ("Malaria is a mosquito-borne infectious disease that affects humans and other animals.", {"entities": [(0, 7, "DISEASE")]}),
                      ("Pneumonia is an infection that inflames the air sacs in one or both lungs.", {"entities": [(0, 9, "DISEASE")]}),
                      ("Tuberculosis is a disease caused by bacteria called Mycobacterium tuberculosis.", {"entities": [(0, 12, "DISEASE")]}),
                      ("Tetanus is a bacterial infection characterized by muscle spasms.", {"entities": [(0, 7, "DISEASE")]}),
                      ("Measles is a highly contagious infectious disease caused by measles virus.", {"entities": [(0, 7, "DISEASE")]}),
                      ("Poliomyelitis is an infectious disease caused by the poliovirus.", {"entities": [(0, 13, "DISEASE")]}),
                      ("Mumps is a viral infection that primarily affects saliva-producing glands that are located near your ears.", {"entities": [(0, 5, "DISEASE")]}),
                      ("Meningitis is an inflammation of the fluid and membranes surrounding your brain and spinal cord.", {"entities": [(0, 10, "DISEASE")]}),
                      ("Chickenpox is a highly contagious disease caused by the initial infection with varicella zoster virus.", {"entities": [(0, 10, "DISEASE")]}),
                      ("Giardiasis is an infection in your small intestine", {"entities": [(0, 10, "DISEASE")]}),
                      ("Covid-19 is a contagious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2).", {"entities": [(0, 8, "DISEASE")]})
                      ]
        # Add the new label to ner
        ner.add_label(LABEL)

        # Resume training
        optimizer = nlp.resume_training()
        move_names = list(ner.move_names)

        # List of pipes you want to train
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

        # List of pipes which should remain unaffected in training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        # Importing requirements
        # Begin training by disabling other pipeline components
        with nlp.disable_pipes(*other_pipes):
            sizes = compounding(1.0, 4.0, 1.001)
            # Training for 30 iterations
            for itn in range(30):
                # shuffle examples before training
                random.shuffle(TRAIN_DATA)
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=sizes)
                # ictionary to store losses
                losses = {}
                for batch in batches:
                    texts, annotations = zip(*batch)
                    # Calling update() over the iteration
                    nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                    print("Losses", losses)"""
        json_load = json.loads(data)
        texts = json_load['text']
        coded = texts.encode('utf-8')
        s = str(coded)
        """print(s[2:-1])"""
        """ Converting text to lowercase """
        arr = s[2:-1]
        small_leter = arr.lower()
        print(small_leter)
        user_id = json_load['id']
        print(user_id)
        """Remove URLs from a sample string"""
        rem_url = re.sub(r"http\S+", "", small_leter)
        """Removing Punctuation marks"""
        rem_punctuation = small_leter.translate(str.maketrans('', '', string.punctuation))
        """print(rem_punctuation)"""
        """Removing white spaces"""
        rem_white = rem_punctuation.strip()
        """print(rem_white)"""
        """Removing stop words"""
        rem_stopwords = remove_stopwords(rem_white)
        """print(rem_stopwords)"""
        """Word Tokenization"""
        doc = nlp(rem_stopwords)
        token_list = []
        for token in doc:
            token_list.append(token)
        """print(token_list)"""
        """Entity Extraction"""
        sp = spacy.load('en_core_web_sm')
        sen = sp(small_leter)
        """print(sen.ents)
        sen = sp(u'Manchester United is looking to sign Harry Kane for $90 million. David demand 100 Million Dollars')"""
        print("Entities using SpaCy")
        for entity in sen.ents:
            print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        print("\nAnnotations using TagMe")
        lunch_annotations = tagme.annotate(small_leter)

        # Print annotations with a score higher than 0.1
        for ann in lunch_annotations.get_annotations(0.1):
            print(ann)
        print("\n Mentions")
        entity_mentions = tagme.mentions(small_leter)

        for mention in entity_mentions.mentions:
            print(mention)
        print("\n")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['Covid-19'], languages=["en"])

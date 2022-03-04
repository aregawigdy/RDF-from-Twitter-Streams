
import tagme
# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = "93eb5238-bf49-4293-84e8-302dcf40944b-843339462"

lunch_annotations = tagme.annotate("My favourite meal is Mexican burritos.")

# Print annotations with a score higher than 0.1
for ann in lunch_annotations.get_annotations(0.1):
    print(ann)
tomatoes_mentions = tagme.mentions("I definitely like ice cream better than tomatoes.")

for mention in tomatoes_mentions.mentions:
    print(mention)
# Get relatedness between a pair of entities specified by title.
rels = tagme.relatedness_title(("Barack Obama", "Italy"))
print("Obama and italy have a semantic relation of", rels.relatedness[0].rel)

# Get relatedness between a pair of entities specified by Wikipedia ID.
rels = tagme.relatedness_wid((31717, 534366))
print("IDs 31717 and 534366 have a semantic relation of ", rels.relatedness[0].rel)

# Get relatedness between three pairs of entities specified by title.
# The last entity does not exist, hence the value for that pair will be None.
rels = tagme.relatedness_title([("Barack_Obama", "Italy"),
                                ("Italy", "Germany"),
                                ("Italy", "BAD ENTITY NAME")])
for rel in rels.relatedness:
    print(rel)

# You can also build a dictionary
rels_dict = dict(rels)
print(rels_dict[("Barack Obama", "Italy")])
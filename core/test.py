'''
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('gtr-t5-base')
sentence = "this is a rock"
embedding = model.encode(sentence, convert_to_tensor=True)
sentences = ["This is a rock", "Could be a stone"] 
embeddings = model.encode(sentences, convert_to_tensor=True)
cosine_scores = util.cos_sim(embedding, embeddings)
print(cosine_scores.squeeze().tolist())
'''
#print("not" in "THis is not ideal".split(" "))
lst = [0.9999999403953552]

print(lst.index(0.99999998403953552))
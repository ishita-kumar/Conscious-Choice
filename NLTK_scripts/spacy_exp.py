from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import pdfplumber

# Load vectors directly from the file
model = KeyedVectors.load_word2vec_format('C:/Users/Chotu/Desktop/Sustainability_Study/NLTK_scripts/data/GoogleNews-vectors-negative300.bin', binary=True)
# Access vectors for specific words with a keyed lookup:
vector = model['easy']
# see the shape of the vector (300,)
vector.shape
# Processing sentences is not as simple as with Spacy:
vectors = [model[x] for x in "This is some text I am processing with Spacy".split(' ')]
text = []
sim = {}
pdf = pdfplumber.open("C:/Users/Chotu/Desktop/Sustainability_Study/NLTK_scripts/data/Ng2015_Article_UnderstandingFoodConsumptionLi.pdf")
for page in pdf.pages:
    each_page = page.extract_text()
    each_page=set(each_page.split(" "))
    for word in each_page: 
        try:
            a= model.similarity('organic',word)
            if a > 0.2:
                sim[word]=a
        except:
            continue

# print(text)
print(sim)

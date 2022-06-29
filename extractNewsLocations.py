import spacy
import ast
import json
# from numpy.compat import unicode


def runNER(locations,  path):
    nlp = spacy.load("en_core_web_sm")
    for loc in locations:
        news_list = []
        for line in open(path + "tempFiles/temporary_" + loc + "_news.txt", "r+"):
            news = ast.literal_eval(line.replace('\n', ''))
            article = news['article']
            doc = nlp(article)
            locationNER = []
            for ent in doc.ents:
                if ent.label_ in ['NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'EVENT']:
                    locationNER.append(str(ent.text+":"+ent.label_))
            news["locationNER"] = ','.join(locationNER)
            news_list.append(news)
        with open(path + "locations_news/" + loc + "_news.txt", 'a+') as locations_news:
            locations_news.write("\n".join(json.dumps(news) for news in news_list))


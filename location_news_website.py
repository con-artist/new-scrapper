import datetime
import json
import re
# import urllib.request
import urllib
from urllib.parse import urljoin
import feedparser
import html
# from html.parser import HTMLParser as hp
from bs4 import BeautifulSoup

class newsSourceSummary1:
    def timesOfIndia(self, soup):
        extraInfo = soup.findAll("img", {"alt": ""})
        data = soup.findAll("div", {"class": "_3YYSt clearfix"})
        extraInfo.extend(data[0].findAll("div", {"class": "_3RArp undefined"}))
        extraInfo.extend([bq.extract() for bq in data[0].findAll("blockquote")])
        for div in data[0].findAll("div", {"class": "_3SEsP"}):
            div.decompose()
            [strong.decompose() for strong in data[0].findAll("strong") if strong.find("a") > 0]
        para = data[0].findAll(text=True)
        text_array = [sentence.strip() for sentence in para]
        text = " ".join(text_array)
        return text, extraInfo


# noinspection PyBroadException,PyUnusedLocal
class newsSourceWebsite:
    def timesOfIndia(self, soup):
        newsDivs = ["col_l_2 col_m_3", "col_l_4 col_m_6", "col_l_1 col_m_4"]
        title = ["figcaption"]
        summary = ["p"]
        return newsDivs, title, summary
 

# noinspection PyGlobalUndefined,PyBroadException,PyUnusedLocal
class newsScrape:
    def getData(self, url, todays_date):
        d = feedparser.parse(url)
        base_url = urljoin(url, '/')

        global news_list
        title = ""
        summary = ""
        link = ""
        date = todays_date
        article = ""
        links_done_count = 0

        for e in d['entries']:
            link = e['link']
            try:
                title = e['title']
            except:
                logs.write(("ERROR (while getting title): " + link + "\n"))

            try:
                summary = e['summary']
                summary = re.sub('<.*?>', '', summary.replace("\n", ""))
            except:
                logs.write(("ERROR (while getting summary): " + link + "\n"))

            # try:
            # link = e['link']
            # if link in news_done:
            # if link in location_link_done_dict[yesterdays_date]:
            #    continue
            flag = False
            for key, val in location_link_done_dict.items():
                if link in val:
                    flag = True
                    break
            if flag:
                continue
                # g.write(link + "\n")
            # print link
            # except:
            #    pass

            try:
                date = e['published']
            except:
                date = datetime.datetime.strptime(todays_date, "%d-%m-%y").strftime('%a, %d %b %Y %H:%M:%S +0000')

            # print link
            loop_count = 0
            while loop_count < 3:
                try:
                    req = urllib.request.Request(link.replace(" ", "%20"))
                    req.add_header('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')
                    r = urllib.request.urlopen(req).read()
                    soup = BeautifulSoup(r, features="html.parser")
                    article, extraInfo = self.getSummary(soup, base_url)
                    # print "Got article" if len(article)>2 else "NADA"
                    article = html.unescape(article)
                    article = re.sub(' +', ' ', article)

                    article_dict = {
                        "title": title.encode('ascii', 'ignore').decode('ascii'),
                        "summary": summary.encode('ascii', 'ignore').decode('ascii'),
                        "article": article.encode('ascii', 'ignore').decode('ascii'),
                        "link": link.encode('ascii', 'ignore').decode('ascii'),
                        "date": date
                    }
                    news_list.append(article_dict)
                    # locations_news.write("\n\n" + "title: " + title + "\n;summary: " + summary + "\n;article: " + article + "\n;link: " + link + "\n;date: " + date + ";".encode('ascii', 'ignore').decode('ascii'))
                    links_done_count += 1
                    location_link_done_dict[todays_date].append(link)
                    break
                except:
                    loop_count += 1
                    # logs.write(("ERROR (while getting article): "+link +"loop_count : "+str(loop_count)+"\n").encode("utf-8"))
            if loop_count == 3:
                logs.write("ERROR (while getting article): ")
                logs.write(str(link.encode("utf-8")))
                logs.write("\n")
                # logs.write('ERROR (while getting article): ' + str(link) + '\n')
        global total_links_done_count
        total_links_done_count += links_done_count
        logs.write(("Articles scraped : " + str(links_done_count) + "\n"))

    def getSummary(self, soup, base_url):
        func = newsSourceSummaryWebsite()
        base_url_functions = {
            "http://www.freepressjournal.in/": func.freePressJournal,
            "http://freepressjournal.in/": func.freePressJournal1,
            "http://www.firstpost.com/": func.firstPost,  # got no link to check
            "http://www.deccanherald.com/": func.deccanHerald,
            "http://timesofindia.feedsportal.com/": func.timesOfIndia,  # check them out later
            "http://timesofindia.indiatimes.com/": func.timesOfIndia,
            "http://www.telegraphindia.com/": func.telegraphIndia,  # solve it later # e[published] not present
            "http://www.newindianexpress.com/": func.newIndianExpress,
            "http://www.dnaindia.com/": func.dnaindia,
            "http://www.thehindu.com/": func.theHindu,
            "https://www.asianage.com/": func.asianage,
            "http://www.tribuneindia.com/": func.tribuneIndia,  # solve it later # lots of redundancy
            "http://indianexpress.com/": func.indianExpress,
            "http://www.mid-day.com/": func.midday,
            "http://post.jagran.com/": func.postjagran,
            "http://www.nagpur-today.com/": func.nagpurtoday,  # got no link to check
            "http://www.timesunion.com/": func.timesunion,
            "http://www.centralchronicle.com/": func.centralchronicle,
            "https://kashmirobserver.net/": func.kashmirobs,
            # not working I think will need to send headers with feedparser
            "http://www.thedelhiwalla.com/": func.delhiwalla,
            "http://www.newsnation.in/": func.newsnation,
            "http://www.ndtv.com/": func.ndtv,  # got no link to check
            "http://www.livemint.com/": func.ht,
            "http://www.financialexpress.com/": func.fe,  # site's feed service is down
            "http://www.frontline.in/": func.frontline,
            "http://www.business-standard.com/": func.businessstandard,
            "https://dc.asianage.com/": func.asiana,  # got no link to check # newspapernot found
            "http://www.lifehacker.co.in/": func.lifehacker,
            "http://www.thestatesman.com/": func.statesman,
            "http://www.gizmodo.in/": func.gizmodo,
            "http://www.onlymyhealth.com/": func.onlymyhealth,  # not required right now. do it later
            "http://www.sportstarlive.com/": func.sportstar,  # site's feed service is down
            "http://www.dailyexcelsior.com/": func.dailyexcel,
            "http://www.espncricinfo.com/": func.espn,
            "http://static.cricinfo.com/": func.cricinfo,  # solve it later # e[published] not present
            "http://www.greaterkashmir.com/": func.gk,  # solve it later # lots of redundancy
            "http://indiatoday.intoday.in/": func.indiatoday,
            # partly solved # e[published] not present in 5th news item
            "http://news.statetimes.in/": func.statetimes,  # site's feed service is down
            "http://www.cricwaves.com/": func.cricw,  # later
            "http://live-feeds.cricbuzz.com/": func.cricbuzz,  # later
            "http://www.news18.com/": func.news18,
            "http://www.indiatvnews.com/": func.indiatv,
            "http://www.ddinews.gov.in/": func.ddnews,
            "http://zeenews.india.com/": func.zeenews,
            "http://www.oneindia.com/": func.oneindia,
            "http://www.filmibeat.com/": func.filmibeat,  # later
            "http://www.goodreturns.in/": func.goodreturns,  # later
            "http://www.gizbot.in/": func.gizbot,  # later
            "http://www.abplive.in/": func.abplive,
            "http://sify.com/": func.sify,
            "http://www.lululovesbombay.com/": func.Bombaylulu,
            "http://www.socialsamosa.com/": func.socialsamosa,
            # "http://www.labnol.org/": func.labnol,
            # "http://timesascent.com/": func.timesascent,
            "http://economictimes.indiatimes.com/": func.et,
            "http://www.bestmediainfo.com/": func.bestmediainfo,
            "http://www.thatdelhigirl.com/": func.thatdelhigirl
        }
        # noinspection PyArgumentList
        article, extraInfo = base_url_functions[base_url](soup)
        return article, extraInfo


# noinspection PyGlobalUndefined
def main(todays_date, locations, path):
    # locations = os.listdir("locations_EPs/")
    # locations = ["delhi_EPs"]
    global total_links_done_count, logs, location_link_done_dict, news_list
    news_list = []
    total_links_done_count = 0
    log_filename = "logs_" + todays_date + ".txt"
    logs = open(path + "logs/" + log_filename, "w+")
    for loc in locations:
        logs.write((loc + ":" + "\n"))

        # locations_news = io.open(path + "locations_news/test_" + loc + "_news", 'a+', encoding='utf-16')
        # g = io.open(path + loc[0]+"_links_done", 'a+', encoding='utf-16')
        # news_done = g.read().split("\n")

        location_link_done_dict = {}
        with open(path + "locations_links_done/" + loc + "_links_done.json", "r+") as data_file:
            location_link_done_dict = json.load(data_file)

        location_link_done_dict[todays_date] = []
        n = newsScrape()
        i = 1
        for ep in open(path + "locations_EPs/" + loc + "_EPs"):
            ep = ep.strip('\n')
            logs.write(("\nnews source " + str(i) + " : " + ep + "\n"))
            n.getData(ep, todays_date)
            i = i + 1

        logs.write("\n\n")
        # with open(path + "locations_news/test_" + loc + "_news", 'a+', encoding='utf-16') as locations_news:
        with open(path + "tempFiles/temporary_" + loc + "_news.txt", 'w') as locations_news:
            locations_news.write("\n".join(json.dumps(news) for news in news_list))

        with open(path + "locations_links_done/" + loc + "_links_done.json", "w") as data_file:
            # dic = json.load(data_file)
            # dic.update(location_link_done_dict)
            json.dump(location_link_done_dict, data_file, sort_keys=True, indent=4)

    logs.write(("\nTotal articles scraped : " + str(total_links_done_count)))
    logs.close()
    # locations_news.close()
    return log_filename

# if __name__ == "__main__":
# yesterdays_date = yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%d-%m-%y")
# link = "https://www.newsnation.in/crime-news/greater-noida-sales-manager-murder-wife-wanted-divorce-to-settle-with-lover-planned-killing-article-222600.html"
# req = urllib.request.Request(link.replace(" ", "%20"))
# req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')
# r = urllib.request.urlopen(req).read()
# soup = BeautifulSoup(r)
# base_url = urljoin(link, '/')
# #print soup
# n = newsScrape()
# article, extraInfo = n.getSummary(soup, base_url)
# print article,"\n\n", extraInfo
# main()
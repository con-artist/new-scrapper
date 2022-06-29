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


# noinspection PyBroadException,PyUnusedLocal
class newsSourceSummary1:
    def freePressJournal(self, soup):
        data = soup.findAll("div", {"itemprop": "articleBody"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def freePressJournal1(self, soup):
        data = soup.findAll("div", {"itemprop": "articleBody"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def firstPost(self, soup):
        data = soup.findAll("div", {"class": "fullCont1"})
        text = ''.join(data[0].findAll(text=True)).replace(
            "&nbsp;", " ").replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def deccanHerald(self, soup):
        data = soup.findAll("div", {"class": "newsText"})
        redundant = soup.find("p", {"class": "gotoTop"})
        if len(redundant) > 0:
            for r in redundant:
                r.extract()
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

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

    def telegraphIndia(self, soup):
        data = soup.findAll("td", {"class": "story"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def newIndianExpress(self, soup):
        text = ""
        extraInfo = []
        try:
            extraInfo = soup.findAll("figure", {"class": "AticleImg"})
            data = soup.findAll("div", {"class": "articlestorycontent"})
            try:
                for strong in data[0].findAll("strong"):
                    extraInfo.append(strong.extract()) if strong.find("a") > 0 else strong.decompose()
            except:
                pass
            try:
                extraInfo.extend(data[0].findAll("img"))
                extraInfo.extend([bq.extract() for bq in data[0].findAll("blockquote")])
            except:
                pass
            para = data[0].findAll("p")
            text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").strip() for sentence in para]
            text = " ".join(text_array)
        except:
            pass
        return text, extraInfo

    def theHindu(self, soup):
        data = soup.findAll("div", {"class": "article"})
        extraInfo = [fig.find("img") for fig in data[0].findAll(
            "div", {"class": "img-container"})]  # Only thumbnail, not able to extract whole image
        content = data[0].find("div", {"id": re.compile(r"content-body")})
        para = [content.find("p")]
        for pr in para[0].find_next_siblings("p"):
            extraInfo.append(
                pr) if pr.text[:9] == "Also read" else para.append(pr)
        text_array = [" ".join(sentence.findAll(text=True)).replace(
            "\n", "").strip() for sentence in para]
        text = " ".join(text_array)
        return text, extraInfo

    def dnaindia(self, soup):
        data = []
        extraInfo = []
        try:
            data = soup.findAll("div", {"class": "article-description"})
        except:
            pass
        try:
            for img in data[0].findAll("img", {"alt": ""}):
                img.decompose()
            [strong.decompose() for strong in data[0].findAll(
                "strong") if strong.find("a") > 0]
            extraInfo = data[0].findAll("img")
        except:
            pass
        text = ""
        try:
            para = data[0].findAll("div", {"class": ""})
            text_array = [" ".join(sentence.findAll(text=True)).replace(
                "\n", "").strip() for sentence in para]
            text = " ".join(text_array)
        except:
            pass
        return text, extraInfo

    def asianage(self, soup):
        data = []
        extraInfo = []
        try:
            extraInfo = soup.findAll("div", {"class": "single-view-banner"})
            data = soup.findAll("div", {"class": "storyBody"})
        except:
            extraInfo = []
            data = []
        try:
            extraInfo.extend(data[0].findAll("blockquote"))
            extraInfo.extend([strong.extract() for strong in data[0].findAll(
                "strong") if strong.find("a") > 0])
        except:
            pass
        text = ""
        try:
            para = data[0].findAll("p")
            text_array = [" ".join(sentence.findAll(text=True)).replace(
                "\n", "").strip() for sentence in para]
            text = " ".join(text_array)
        except:
            pass
        return text, extraInfo

    def tribuneIndia(self, soup):
        data = soup.findAll("div", {"class": "Storyleft"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def indianExpress(self, soup):
        text = ""
        try:
            data = soup.findAll("div", {"id": "pcl-full-content"})
            para = data[0].findAll("p")
            text_array = [" ".join(sentence.findAll(text=True)).replace(
                "\n", "").strip() for sentence in para]
            text = " ".join(text_array)
        except:
            pass
        return text, []

    def midday(self, soup):
        extraInfo = soup.findAll("div", {"class": "atrFirstImg"})
        data = soup.findAll("div", {"class": "articlebody"})
        for strong in data[0].findAll("strong"):
            extraInfo.append(strong.extract()) if strong.find(
                "a") > 0 else strong.decompose()
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True, recursive=False)).replace("\n", "") for sentence in para]
        text = " ".join(text_array)
        return text, extraInfo

    def postjagran(self, soup):
        extraInfo = soup.findAll("div", {"class": "stryimg"})
        data = soup.findAll("div", {"class": "article-body"})
        extraInfo.extend([bq.extract() for bq in data[0].findAll("blockquote")])
        para = data[0].find("p", {"class": "stry-dt"}).findAll("p")
        extraInfo.extend([sentence.find("img").extract() for sentence in para if sentence.find("img")])
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").strip() for sentence in para]
        text = " ".join(text_array)
        return text, extraInfo

    def nagpurtoday(self, soup):
        data = soup.findAll("div", {"class": "post"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def timesunion(self, soup):
        data = soup.findAll("div", {"class": "article-body"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def centralchronicle(self, soup):
        data = soup.findAll("div", {"class": "entry entry-content"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace(
            "\n", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def kashmirobs(self, soup):
        data = soup.findAll("div", {"class": "articlebody"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def delhiwalla(self, soup):
        data = soup.findAll("div", {"class": "entry-content"})
        [strong.decompose() for strong in data[0].findAll("strong")]
        extraInfo = data[0].findAll("img")
        para = data[0].findAll("p", recursive=False)
        text_array = [" ".join(sentence.findAll(text=True, recursive=False)).strip() for sentence in para]
        text = " ".join(text_array)
        return text, extraInfo

    # def delhiwalla(self, soup):
    #     try:
    #         data = soup.findAll("div", {"class": "entry-content"})
    #         # [strong.decompose() for strong in data[0].findAll("strong")]
    #         extraInfo = data[0].findAll("img")
    #         para = data[0].findAll("p", recursive=False)
    #         text_array = [" ".join(sentence.findAll(text=True, recursive=False)).strip() for sentence in para]
    #         text = " ".join(text_array)
    #     except:
    #         text = ""
    #         extraInfo = []
    #     return text, extraInfo
    def newsnation(self, soup):
        data = []
        extraInfo = []
        try:
            images = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['rel'])
            extraInfo = images.findAll("img") if images is not None else []
        except:
            pass
        try:
            data = soup.findAll("div", {"class": "art-txt"})
            extraInfo.extend(data[0].findAll("img"))
        except:
            pass
        try:
            for strong in data[0].findAll("strong"):
                extraInfo.append(strong.extract()) if strong.find(
                    "a") > 0 else strong.decompose()
            extraInfo.extend([bq.extract() for bq in data[0].findAll("blockquote")])
        except:
            pass
        try:
            para = data[0].findAll("p")
            text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "").strip() for sentence in para]
            text = " ".join(text_array)
        except:
            text = ""
        return text, extraInfo

    def ndtv(self, soup):
        data = soup.findAll("div", {"class": "ins_storybody"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def ht(self, soup):
        data = soup.findAll("div", {"id": "div_storyContent"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace(
            "\n", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def fe(self, soup):
        data = soup.findAll("div", {"class": "main-story-content"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def frontline(self, soup):
        try:
            data = soup.findAll("div", {"class": "content"})
            para = data[0].findAll("p")
        except:
            data = soup.findAll("div", {"id": "articlepage"})
            para = data[0].findAll("p")

        text_array = [" ".join(sentence.findAll(text=True)).replace(
            "\n", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def businessstandard(self, soup):
        data = soup.findAll("div", {"class": "story-content"})
        try:
            for d in data:
                if d.find("div", {"class": "row-inner"}):
                    raise Exception

            para = data[0].findAll("p")

            array = []
            for sentence in para:
                sents = sentence.findAll(text=True)
                array.extend(sents)

            text_array = []
            before = 0
            after = 0
            for i in range(len(array)):
                if "document.write" in array[i]:
                    before = i
                elif "INPAGE_BANNER" in array[i]:
                    after = i + 1
            text_array = array[:before] + array[after:]
            text = " ".join(text_array).replace(
                "\n", "").replace("\r", "").replace("\t", "")
        except:
            text = ""
        extraInfo = []
        return text, extraInfo

    def asiana(self, soup):
        data = soup.findAll("div", {"class": "content"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def lifehacker(self, soup):
        data = soup.findAll("div", {"class": "Normal"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def statesman(self, soup):
        data = soup.findAll("div", {"class": "stroy"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace(
            "\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def espn(self, soup):
        para = []
        data = soup.find("p")
        while True:
            try:
                if data.name == "div":
                    break
                else:
                    para.append(data.text.replace("\n", ""))
                    data = data.nextSibling
            except:
                data = data.nextSibling

        if "espni" in para[0]:
            para = para[1:]

        text = " ".join(para)
        extraInfo = []
        return text, extraInfo

    def cricinfo(self, soup):
        data = soup.findAll("div", {"class": "row brief-summary"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def gizmodo(self, soup):
        data = soup.findAll("div", {"class": "Normal"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def onlymyhealth(self, soup):
        data = soup.findAll("div", {"class": "beauty-tips"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def dailyexcel(self, soup):
        data = soup.findAll("div", {"class": "entry-content"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def sportstar(self, soup):
        data = soup.findAll("div", {"class": "articleBody"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def gk(self, soup):
        data = soup.findAll("span", {"class": "storyText"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def indiatoday(self, soup):
        data = soup.findAll("div", {"class": "right-story-container"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def statetimes(self, soup):
        data = soup.findAll("div", {"class": "pf-content"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def cricw(self, soup):
        data = soup.findAll("div", {"class": "blgd bldg_content"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def cricbuzz(self, soup):
        data = soup.findAll(
            "div", {"class": "cb-col cb-col-100 cb-mini-col cb-min-comp ng-scope"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def news18(self, soup):
        data = soup.findAll("div", {"id": "article_body"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def indiatv(self, soup):
        data = soup.findAll("div", {"id": "mad-con-new"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def oneindia(self, soup):
        data = soup.findAll("div", {"class": "ecom-ad-content"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def zeenews(self, soup):
        data = soup.findAll("div", {"class": "full-con"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para if
                      not sentence.find("div")]
        text = " ".join(text_array)
        extraInfo = []
        return text, extraInfo

    def ddnews(self, soup):
        data = soup.findAll(
            "div", {"id": "ctl00_PlaceHolderMain__migidNBody__ControlWrapper_RichHtmlField"})
        text = ''.join(data[0].findAll(text=True)).replace(
            "\n", " ").replace("\r", " ")
        extraInfo = []
        return text, extraInfo

    def filmibeat(self, soup):
        data = soup.findAll("div", {"class": "filmibeat-fullcontent"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")

    def goodreturns(self, soup):
        data = soup.findAll("div", {"class": "new_main_story_width"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def gizbot(self, soup):
        data = soup.findAll("div", {"class": "article-contents-block"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def abplive(self, soup):
        text = ""
        try:
            data = soup.findAll("div", {"class": "_picCon"})
            para = data[0].findAll("p")
            text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in
                          para]
            text = " ".join(text_array)
        except:
            pass
        extraInfo = []
        return text, extraInfo

    # def sify(self, soup):
    #     data = soup.findAll("div", {"class": "fullstory-txt"})
    #     para = data[0].findAll("p")
    #     text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
    #     text = " ".join(text_array)
    #     text = re.sub('sify(.*?);', '', text)
    #     extraInfo = []
    #     return text, extraInfo

    # def Bombaylulu(self, soup):
    #     data = soup.findAll("div", {"class": "article-content entry-content"})
    #     text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
    #     extraInfo = []
    #     return text, extraInfo

    def socialsamosa(self, soup):
        data = soup.findAll("div", {"class": "theiaPostSlider_slides"})
        text = ""
        try:
            data = soup.findAll("div", {"class": "_picCon"})
            para = data[0].findAll("p")
            text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in
                          para]
            text = " ".join(text_array)
        except:
            pass
        extraInfo = []
        return text, extraInfo

    def sify(self, soup):
        data = soup.findAll("div", {"class": "fullstory-txt"})
        para = data[0].findAll("p")
        text_array = [" ".join(sentence.findAll(text=True)).replace("\n", "").replace("\r", "") for sentence in para]
        text = " ".join(text_array)
        text = re.sub('sify(.*?);', '', text)
        extraInfo = []
        return text, extraInfo

    def Bombaylulu(self, soup):
        data = soup.findAll("div", {"class": "article-content entry-content"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    # def socialsamosa(self, soup):
    #     data = soup.findAll("div", {"class": "theiaPostSlider_slides"})

    def et(self, soup):
        data = soup.findAll("div", {"class": "Normal"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def bestmediainfo(self, soup):
        data = soup.findAll("div", {"class": "detail_page"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo

    def thatdelhigirl(self, soup):
        data = soup.findAll("div", {"id": "content-area"})
        text = ''.join(data[0].findAll(text=True)).replace("\n", " ")
        extraInfo = []
        return text, extraInfo


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
        func = newsSourceSummary1()
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

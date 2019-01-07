import re
import urllib.request
import json

class StringProcessor:

    def __init__(self):
        pass

    def updateHTML(self, html):
        self._html = html

    def chunkSentences(self, data):
        return self._separateSentences(data)

    def _separateSentences(self, data):

        #sub in newline on sentence end punctuation
        data = re.sub(r'[\!\.\?]','\n', data)

        #separate on newline character
        separated = data.split('\n')

        #return list of chunked sentences without punctuation
        return [self._stripPunctuation(x) for x in separated if x]

    def _stripPunctuation(self, sentence):
        #strip punctuation
        sentence = re.sub(r'[^\w\s\']','', sentence)

        #remove non-ascii and non-utf8
        sentence = re.sub(r'[^\x00-\x7F]+|[\u00D8-\u00F6]+',' ', sentence)

        #remove weird character
        sentence = re.sub(r'[\t]+',' ', sentence)

        #chunk sentence into list
        sentence = sentence.split()

        #lower
        return [x.lower() for x in sentence]

    def cleanHTML(self, isWiki):

        #concatenate all text (weird new line characters in html)
        self._concatenateHTML()

        #remove unwanted html tags
        self._stripUnwantedHTML(isWiki)

        self._stripHTMLTags()

        return self._html

    def _wikipediaContent(self):
        #locate the body content div
        self._html = re.search(r'(<div id=\"bodyContent\" class=\"mw-body-content\">.+<div id=\"mw-navigation\">)', self._html).group(0)

        #get rid of the edits
        self._html = re.sub(r'\[.+?\]', ' ', self._html)

    def _concatenateHTML(self):
        self._html = re.sub(r'(\r\n|\r|\n)',' ', self._html)

    def _stripUnwantedHTML(self, isWiki):

        if isWiki:
            self._wikipediaContent()

        self._html = re.sub(r'(<script.+?script>|<style.+?style>|<title.+?title>|<head.+?head>|<link.+?>|<meta.+?>|<img.+?>|<table.+?table>|<span.+?span>|<semantics.+?semantics>|<noscript.+?noscript>|<sup.+?sup>)',' ', self._html)

    def _stripHTMLTags(self):
        self._html = re.sub(r'<.+?>',' ', self._html)


class MyHTMLParser:

    def __init__(self, isWiki):
        self.isWiki = isWiki
        self._data = []
        self._StringProcessor = StringProcessor()

    def getData(self):
        return self._data

    def grabTextURL(url):

        #fetch html in bytes
        fp = urllib.request.urlopen(url)
        htmlBytes = fp.read()

        #convert to strings
        htmlStr = htmlBytes.decode('utf-8', 'ignore')
        fp.close()

        return htmlStr

    def feed(self, html):
        self._StringProcessor.updateHTML(html)
        cleanHTML = self._StringProcessor.cleanHTML(self.isWiki)
        self._data.extend(self._StringProcessor.chunkSentences(cleanHTML))

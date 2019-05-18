import re

import html2text

from ._abstract import AbstractRecipe

_BASE_URL = 'https://www.vogue.com/'


class Recipe(AbstractRecipe):

    def _extract_authors(self):
        self._output['authors'] = (
            [self._soup.find('a', class_='contributor-byline--name').text])

    def _extract_category(self):
        self._output['category'] = (
            self._soup.find('a', itemprop='articleSection').text)

    def _extract_content(self):
        content = ''
        paragraphs = (
            self._soup.find('div', class_='article-copy--body').find_all(
                ['div', 'p'], recursive=False))
        # To avoid lines cropping, see:
        # https://stackoverflow.com/questions/12839143/python-html2text-adds-random-n
        converter = html2text.HTML2Text()
        converter.body_width = 0
        for paragraph in paragraphs:
            if paragraph.name == 'p':
                content += converter.handle(str(paragraph))
            elif (
                paragraph.name == 'div'
                    and 'image-embed' in paragraph['class']):
                srcset = paragraph.find_all('source')[0]['srcset']
                images = re.search('http.+?\.\w{1,3},', srcset)
                if images:
                    content += '![]({})'.format(images.group(0)[0:-1])
        content = content.replace('](/', ']({}'.format(_BASE_URL))
        self._output['content'] = content

    def _extract_image(self):
        # It assumes the first <source> contains the primary image.
        srcset = self._soup.find_all('source')[0]['srcset']
        images = re.search('http.+?\.\w{1,3},', srcset)
        if images:
            self._output['image'] = images.group(0)[0:-1]

    def _extract_published(self):
        el = self._soup.find('time', class_='article-content-meta--date')
        timestr = el['datetime']
        self._output['published'] = timestr[0:10]

    def _extract_tags(self):
        self._output['tags'] = (
            [el.text
             for el in self._soup.find_all('a', class_='article-tags--link')])

    def _extract_title(self):
        self._output['title'] = (
            self._soup.find('h1', class_='article-content--title').text)

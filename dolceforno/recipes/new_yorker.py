import datetime
import re

import html2text

from ._abstract import AbstractRecipe

_BASE_URL = 'https://www.newyorker.com/'


class Recipe(AbstractRecipe):

    def _extract_authors(self):
        self._output['authors'] = [self._soup.find('a', rel='author').text]

    def _extract_category(self):
        regex = re.compile(r'ArticleHeader__rubric__')
        self._output['category'] = self._soup.find('div', class_=regex).text

    def _extract_content(self):
        article = self._soup.find('div', id='articleBody')
        paragraphs = article.find_all('p')

        content = ''
        for paragraph in paragraphs:
            classes = paragraph.get('class') or []
            classes_str = ''.join(classes)
            classes_skip = ['Carousel', 'Byline']
            if not any([c in classes_str for c in classes_skip]):
                converter = html2text.HTML2Text()
                converter.body_width = 0
                content += converter.handle(str(paragraph))
        self._output['content'] = content

    def _extract_image(self):
        self._output['image'] = self._soup.find('picture').find('img')['src']

    def _extract_published(self):
        timestr = (
            self._soup.find('p', class_=re.compile(r'ArticleTimestamp')).text)
        # Example: 5:00 A.M.
        if '.' in timestr:
            timestamp = datetime.datetime.now()
        # Example: April 1, 2019.
        else:
            # Library datetime can only parse 0-padded days. Thus, we need to
            # extract the day and 0-pad it if necessary.
            regex = re.search(r'(\w{3,12}) (\d{1,2}), (\d{4})', timestr)
            month = regex.group(1)
            day = (regex.group(2)
                   if len(regex.group(2)) == 2
                   else '0' + regex.group(2))
            year = regex.group(3)
            timestr = '{}-{}-{}'.format(day, month, year)
            timestamp = datetime.datetime.strptime(timestr, '%d-%B-%Y')
        self._output['published'] = timestamp.strftime('%Y-%m-%d')

    def _extract_tags(self):
        items = self._soup.find('ul', class_=re.compile(r'Tags'))
        self._output['tags'] = [item.text for item in items.find_all('li')]

    def _extract_title(self):
        self._output['title'] = self._soup.find('h1').text

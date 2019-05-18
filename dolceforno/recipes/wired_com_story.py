import html2text

from ._abstract import AbstractRecipe

_BASE_URL = 'https://www.wired.com/'


class Recipe(AbstractRecipe):

    def _extract_authors(self):
        self._output['authors'] = [self._soup.find('a', rel='author').text]

    def _extract_category(self):
        self._output['category'] = (
            self._soup.find('div', class_='brow-component').find('a').text)

    def _extract_content(self):
        article = self._soup.find('article', class_='article-body-component')
        paragraphs = article.find_all('p')

        content = ''
        for paragraph in paragraphs:
            converter = html2text.HTML2Text()
            converter.body_width = 0
            content += converter.handle(str(paragraph))

        self._output['content'] = content

    def _extract_image(self):
        try:
            self._output['image'] = (
                self._soup.find('figure').find('img')['src'])
        except AttributeError:
            pass

    def _extract_published(self):
        mdy = self._soup.find('time', class_='date-mdy').text
        # The following solution will only work until 2090.
        year = '20'+mdy[6:8] if not mdy[6:8].startswith('9') else '19'+mdy[6:8]
        self._output['published'] = (
            '{yyyy}-{mm}-{dd}'.format(yyyy=year, mm=mdy[0:2], dd=mdy[3:5]))

    def _extract_tags(self):
        div = self._soup.find('div', class_='tags-component')
        items = div.find('ul').find_all('li')
        self._output['tags'] = [
            item.find('a').text.replace('#', '')
            for item in items
        ]

    def _extract_title(self):
        self._output['title'] = (
            self._soup.find('h1', id='articleTitleFull').text)

import html2text

from ._abstract import AbstractRecipe

_BASE_URL = 'https://www.wired.com/'


class Recipe(AbstractRecipe):

    def _extract_authors(self):
        self._output['authors'] = [self._soup.find('a', rel='author').text]

    def _extract_category(self):
        self._output['category'] = self._soup.find(
            'span', class_='category-meta').find('a').text

    def _extract_content(self):
        article = self._soup.find('article', class_='content')
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
        self._output['published'] = self._soup.find(
            'meta', itemprop='datePublished')['content'][0:10]

    def _extract_tags(self):
        try:
            items = self._soup.find('ul', id='article-tags').find_all('li')
            self._output['tags'] = [item.find('a').text for item in items]
        except AttributeError:
            self._output['tags'] = []

    def _extract_title(self):
        self._output['title'] = self._soup.find('h1', class_='post-title').text

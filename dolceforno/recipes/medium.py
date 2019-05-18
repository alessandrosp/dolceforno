import html2text

from ._abstract import AbstractRecipe


class Recipe(AbstractRecipe):

    def _extract_authors(self):
        self._output['authors'] = [self._soup.find('a', class_='ds-link').text]

    def _extract_category(self):
        pass

    def _extract_content(self):
        sections = self._soup.find_all('div', class_='section-inner')

        paragraphs = []
        for section in sections:
            paragraphs += section.find_all(['figure', 'h2', 'h3', 'p'])

        content = ''
        for paragraph in paragraphs:
            converter = html2text.HTML2Text()
            converter.body_width = 0
            content += converter.handle(str(paragraph))

        self._output['content'] = content

    def _extract_image(self):
        self._output['image'] = (
            self._soup.find('img', class_='graf-image')['src'])

    def _extract_published(self):
        el = self._soup.find('time')
        timestr = el['datetime']
        self._output['published'] = timestr[0:10]

    def _extract_tags(self):
        items = self._soup.find('ul', class_='tags').find_all('li')
        self._output['tags'] = [item.text for item in items]

    def _extract_title(self):
        self._output['title'] = self._soup.find('h1').text

import collections
import re

import bs4


class AbstractRecipe(object):
    def __init__(self):
        self._soup = None
        self._output = collections.defaultdict(str)

    def _clean_content(self):
        self._output['content'] = self._output['content'].replace(' _,', '_,')
        self._output['content'] = self._output['content'].replace(' ,', ',')
        self._output['content'] = (
            re.sub(r'\n{1,}', '\n\n', self._output['content']))

    def _output_is_valid(self):
        if len(self._output['title']) < 3:
            raw_message = 'WARNING: The title as parsed was too short: {}'
            message = raw_message.format(self._output['title'])
            print(message)
            return False
        if len(self._output['content']) < 42:
            raw_message = (
                'WARNING: The content as parsed was too short, '
                'only {} characters.')
            message = raw_message.format(len(self._output['content']))
            print(message)
            return False
        # Published date can be omitted but it's present then
        # it's has to be in the format YYYY-MM-DD.
        if self._output['published'] and len(self._output['published']) != 10:
            print('WARNING: The title as parse was too short.')
            return False
        return True

    def parse(self, html):
        self._soup = bs4.BeautifulSoup(html, 'html.parser')
        if self._soup:
            self._extract_authors()
            self._extract_category()
            self._extract_content()
            self._clean_content()
            self._extract_image()
            self._extract_published()
            self._extract_tags()
            self._extract_title()
        if self._output_is_valid():
            return self._output
        return None

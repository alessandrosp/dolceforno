import importlib
import os
import sys
import unittest

import pandas as pd
from parameterized import parameterized

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
import dolceforno  # noqa: E402

_URLS_FILEPATH = 'tests/unit/dolceforno_urls.csv'
_URLS_DATAFRAME = pd.read_csv(_URLS_FILEPATH)


class TestDolceForno(unittest.TestCase):

    @parameterized.expand([tuple(u) for u in _URLS_DATAFRAME.values])
    def test_select_appropriate_recipe(self, url, path):
        recipe = dolceforno.select_appropriate_recipe(url)
        module = importlib.import_module(path, package=None)
        self.assertIsInstance(recipe, module.Recipe)


if __name__ == '__main__':
    unittest.main()

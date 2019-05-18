import importlib
import json
import os
import sys
import unittest

from parameterized import parameterized

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
import dolceforno  # noqa

_ASSETS_FOLDERPATH = 'tests/unit/assets/'


def create_input_output_tuples():
    """Creates a list of (input, output) tuples.

    Returns:
        A list of tuples.
    """
    input_output_tuples = []
    recipe_names = os.listdir(_ASSETS_FOLDERPATH)
    for recipe_name in recipe_names:
        file_names = os.listdir(os.path.join(_ASSETS_FOLDERPATH, recipe_name))
        for file_name in file_names:
            if '.html' in file_name:
                input_file = os.path.join(
                    os.path.join(_ASSETS_FOLDERPATH, recipe_name), file_name)
                output_file = input_file.replace('.html', '.json')
                input_output_tuples.append((input_file, output_file))
    return input_output_tuples


def extract_recipe_name(input_filepath):
    return input_filepath.split('/')[-2]


class TestRecipes(unittest.TestCase):

    @parameterized.expand(create_input_output_tuples())
    def test_recipes(self, input_filepath, output_filepath):
        with open(input_filepath, 'r') as input:
            html = input.read()
        recipe_path = 'recipes.{}'.format(extract_recipe_name(input_filepath))
        recipe = importlib.import_module(recipe_path, package=None).Recipe()
        result = recipe.parse(html)
        with open(output_filepath, 'r') as output:
            expected = json.load(output)
        # Note that result is a collection.defaultdict() while expected
        # is a dict(). This is not an issue.
        self.assertDictEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

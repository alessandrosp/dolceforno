# DolceForno: High-Precision Scraping Library

## Introduction

**DolceForno is a library to scrape articles from all around the web.** Contrary
to other available libraries, DolceForno doesn't use a one-size-fits-all
set of rules nor it relies on machine learning algorithms. Instead, it uses a
series of bespoke recipes manually created for each publications. Because of
this DolceForno offers high-precision low-recall scraping (as no all
publications are supported; see below for more details).

DolceForno will try to scrape the following information from the article:

- The author(s) of the article.
- The category the article was posted under, if any.
- The article itself in markdown syntax, including the images (but for the
primary image, which is stored separately).
- The primary image.
- The date the article was published, e.g. `2019-12-31`.
- The tags of the articles, if any.
- The title of the article.

The only two fields that are absolutely mandatory are `title` and `content`.

## Usage

The simplest way to use DolceForno is to simply pass it a URL.

```python
import dolceforno

url = 'https://www.vogue.com/article/joan-didion-self-respect-essay-1961'
dolce_forno = dolceforno.DolceForno(url)
output = dolce_forno.cook()  # Output is a dict.
```

You can also save the output to disk as a JSON.

```python
import dolceforno

url = 'https://www.vogue.com/article/joan-didion-self-respect-essay-1961'
dolce_forno = dolceforno.DolceForno(url)
output = dolce_forno.cook()

output_filepath = 'scraped/joan-didion-self-respect-essay-1961.json'
dolce_forno.save(output, output_filepath)
```

There's also a `cook_and_save()` method for convenience.

```python
import dolceforno

url = 'https://www.vogue.com/article/joan-didion-self-respect-essay-1961'
output_filepath = 'scraped/joan-didion-self-respect-essay-1961.json'
dolce_forno = dolceforno.DolceForno(url)
dolce_forno.cook_and_save(output_filepath)
```

If you already have the HTML you can pass it with the appropriate recipe to
`cook()` so that DolceForno doesn't make an additional request.

```python
import dolceforno

url = 'https://www.vogue.com/article/joan-didion-self-respect-essay-1961'
html = '<html>...'
dolce_forno = dolceforno.DolceForno()
recipe = dolceforno.select_appropriate_recipe(url)
output = dolce_forno.cook(html, recipe)
```

Note that `dolceforno.py` can also be used as a command-line tool. The
following command will output two files, one containing the original HTML
code of the article and the other the scraped and parsed content (as a JSON).

```bash
python dolceforno/dolceforno.py -u https://www.vogue.com/article/joan-didion-self-respect-essay-1961 -s
```

The following flags are available for the command-line tool:

- **--url** (or **-u**) to pass the URL to scrape.
- **--output_filepath** (or **-o**) to specify the output location (optional).
- **--save_html** (or **-s**) to save the original HTML code (optional).

## Publications

These are the publications DolceForno currently supports:

- medium.com/
- newyorker.com/
- vogue.com/article/
- wired.com/[YYYY]/[MM]/
- wired.com/story/

Is DolceForno missing your favourite publication? Consider adding it yourself!

## Contribute

Adding new recipes to DolceForno is extremely simple. A typical commit
would touch on 4 files, they are:

- `dolceforno/recipes/<new-recipe>.py`
- `dolceforno/dolceforno.py`
- `tests/unit/dolceforno_urls.csv`
- `tests/unit/assets/<new-recipe>/...`

### `dolceforno/recipes/<new-recipe>.py`

This is where your scraping logic should live. The file should contain a
`Recipe` class that inherits from `AbstractRecipe` and implements 7 methods:

- `_extract_authors()`
- `_extract_category()`
- `_extract_content()`
- `_extract_image()`
- `_extract_published()`
- `_extract_tags()`
- `_extract_title()`

#### `_extract_authors()`

- Type: [str]
- Optional: Yes

It extracts the authors of the article. Because any article could potentially
be written by multiple authors, this is expected to be a list of strings.

#### `_extract_category()`

- Type: str
- Optional: Yes

The category the article was posted under. Many websites don't have categories
so it's perfectly fine for this to be empty. It's a string.

#### `_extract_content()`

- Type: str
- Optional: No

The content of the article in markdown syntax. The `html2text` package
is expected to be used to convert the HTML into valid markdown. Note that
`AbstractRecipe` implements some cleaning logic so that you don't need to worry
about that yourself (e.g., remove spaces before commas).

#### `_extract_image()`

- Type: str
- Optional: Yes

The URL of the primary image for the article. All other images appearing
in the article should instead be stored in `content` in markdown syntax
(e.g. `!()[http://example.com/image.png]`). The URL should be absolute.

#### `_extract_published()`

- Type: str
- Optional: Yes

The date as a string in the format `YYYY-MM-DD`, e.g. `2019-12-31`. This is the
only format accepted so if it's not possible to use this format (e.g., only
the year is available; a very edge case) the field should be empty instead.

#### `_extract_tags()`

- Type: [str]
- Optional: Yes

The tags of the article as a list of strings.

#### `_extract_title()`

- Type: str
- Optional: No

The title of the article.

### `dolceforno/dolceforno.py`

You'll simply need to add a new regex/path pair to `RECIPES_MAPPING`. This is
needed for DolceForno to be able to automatically identify the appropriate
recipe to use for the given URLs.

### `tests/unit/dolceforno_urls.csv`

Used to test that DolceForno is matching the correct recipe to the given URLs.
Simply add 3 URLs and the corresponding recipe to the list. Please, add
your `URLs,recipe` pairs so that all URLs are sorted alphabetically (don't just
add them at the end of the file).

Note that these should be real, valid URLs.

### `tests/unit/assets/<new-recipe>/...`

The scraping logic is tested on 3 articles available locally. These articles
have to be added to /assets/ in a folder that has the name of your recipe. The
folder should contain 6 files: 3 `.html` and 3 `.json`. These are the input
and the output of the tests respectively.

Note that you can quickly generate these files by using `dolceforno.py` as
a command-line tool (see [Usage](#usage) for more details).

```bash
python dolceforno/dolceforno.py -u [URL] -s
```

### Test your code!

Before submiting any code for review, make sure all tests run fine. From
DolceForno main directory (the parent of `dolceforno` and `tests`) execute
`run_all_tests.sh` by running:

`./tests/run_all_tests.sh`

If all suites return an OK status than your code is good to go!

# Project Setup

## Set up the Tooling

First, of course, fork and clone the repo on GitHub.

We use [Poetry](https://python-poetry.org/) to manage our development virtual
environment. This must be installed before starting development on pyZohoAPI.

Once installed, you can set up the virtual environment:

```{code-block} console
$ git clone https://github.com/{your-name}/pyZohoAPI.git
...snip...
$ cd pyZohoAPI
$ poetry install
...snip...
```

Poetry will install all the packages needed, but they're also mentioned below
for completeness.

See the [Poetry docs](https://python-poetry.org/) for more.

## Tooling for Testing

We use [pytest](https://docs.pytest.org/en/stable/) for testing.

Tests rely on a python module **NOT INCLUDED IN THIS REPOSITORY** called
`private` which exports a dictionary called `testdata`, something like:

```{code-block} python
from pyzohoapi.core.collection import DottedDict
testdata = DottedDict({
    'orgid': "your-org-id",
    'region': "your-region",
    'api': {
     "access_token": None,
     "refresh_token": "your-refresh-token",
     "expires_in": 0,
     "client_id": "your-client-id",
     "client_secret": "your-client-secret",
     "redirect_url": None,
    },
    'books': { ... },
    'inventory': { ... },
    ...
})
```

```{danger}
The tests rely on actual secrets data to interact with the live Zoho APIs, and
it's a REALLY BAD IDEA to publish those, so our `.gitignore` specifically
ignores the `private/` directory, and that's where we look for these secrets.
```

In order to run the tests, you must create `private/__init__.py` with at least
the data indicated above, and add those key/value pairs the tests themselves
require. See the tests codes themselves for the details.

To run the tests:

```{code-block} console
poetry run pytest
```

Or, a particular test, such as one you added:

```{code-block} console
poetry run pytest -k my_test_name
```

All the tests are under the `tests` directory, naturally. Contained therein are:

* `__init__.py` - lets Python consider the tests part of a module.
* `test_00_pyzohoapi.py` - tests for the primitives in the ZohoAPI base class.
* `test_inventory{_.*}.py` - tests specifically for ZohoInventory.

Tests you add should follow the same pattern; Additional tests for
the already-present APIs should either be added into the existing `test_...`
file, or a new one of the form `test_{api}_{seq}.py`

## Tooling for Documentation

All documentation is written in Markdown.

We use:

* [Sphinx](https://www.sphinx-doc.org/en/master/) - the documentation engine
* [Myst](https://github.com/executablebooks/MyST-Parser) - adds Markdown support to Sphinx
* [Furo](https://github.com/pradyunsg/furo) - a lovely simple theme
* [sphinx-autobuild](https://pypi.org/project/sphinx-autobuild/) - builds docs and gives us a live-reloading web server
* [sphinx-copybutton](https://sphinx-copybutton.readthedocs.io/en/latest/) - add copy-to-clipboard to code blocks

To use sphinx-autobuild:

```{code-block} console
poetry run sphinx-autobuild docs docs/build/html --open-browser --watch .
```

## Commits, Versioning and ChangeLog

We adhere to [Semantic Versioning](https://semver.org) and [Conventional
Commits](https://www.conventionalcommits.org/)<sup>*</sup> and apply the
principles espoused on [Keep A Changelog](https://keepachangelog.com).

We use [BumpyTrack](https://github.com/nandilugio/bumpytrack) for versioning,
thus:

```{code-block} console
bumpytrack {aspect} --config-path bumpytrack.toml
```

Of course, `{aspect}` should be `major`, `minor` or `patch` depending on the
actual aspect we are bumping.

We use [Git-Changelog](https://github.com/pawamoy/git-changelog) to generate our
CHANGELOG.md, thus:

```{code-block} console
git-changelog . -o CHANGELOG.md
```

Naturally, pull-requests will be bumped/changelogged by the maintainer(s), but
if you're going to issue a pull request, please ensure your commit messages will
be parsed properly.

_<sup>*</sup>Going forward. Previous commits may not._

## Helpful Dev and Debug Tools

There are two tools in the `tools` directory to make development and testing
(hopefully) easier.

```{note}
Both of these tools rely on the `private` module mentioned above.
```

### Interactive Test Server

The Interactive Test Server spins up a simple web server on
http://localhost:8080. This allows you to send queries to the Zoho APIs and see
the JSON response data.

```{code-block} console
poetry run python tools/interactive-test-server.py
```

You can add `--port` and a port number to the above to override the
default port (8080).

If you want to see the log entries the library is making, add `--log` to the
above.

### Interactive Shell

The Interactive Shell launches a Python REPL with pyzohoapi pre-loaded and
confgured (see the section on `private`, above).

```{code-block} console
poetry run python -i tools/test-shell.py
```

```{note}
Don't forget the `-i` in the command above to get your interactive shell.
```

```{code-block} console
testshell()
    Test shell loaded. Here's what you have:

    Modules:
        decimal.Decimal (as Decimal);
        json (simplejson, aliased to json);

    Functions:
        pprint();
        show(object, key=None) -> shows a Zoho Object (or optional attribute);

    Objects:
        private.testdata -> dict, aliased to td;
        books -> ZohoBooks object : configured via testdata;
        inv -> ZohoInventory object : configured via testdata;

    Type: help(testshell) to get this help again.

    Enjoy your testing!

>>> inv.Item('9876543210987654321')
Item #9876543210987654321
>>>
```

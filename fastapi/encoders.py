import dataclasses
import datetime
from collections import defaultdict, deque
from decimal import Decimal
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path, PurePath
from re import Pattern
from types import GeneratorType
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from uuid import UUID

from fastapi.types import IncEx
from pydantic import BaseModel
from pydantic.color import Color
from pydantic.networks import AnyUrl, NameEmail
from pydantic.types import SecretBytes, SecretStr
from typing_extensions import Annotated, Doc

from ._compat import PYDANTIC_V2, UndefinedType, Url, _model_dump


# Taken from Pydantic v1 as is
def isoformat(o: Union[datetime.date, datetime.time]) -> str:
    return o.isoformat()


# Taken from Pydantic v1 as is
# TODO: pv2 should this return strings instead?
def decimal_encoder(dec_value: Decimal) -> Union[int, float]:
    """
    Encodes a Decimal as int of there's no exponent, otherwise float

    This is useful when we use ConstrainedDecimal to represent Numeric(x,0)
    where a integer (but not int typed) is used. Encoding this as a float
    results in failed round-tripping between encode and parse.
    Our Id type is a prime example of this.

    >>> decimal_encoder(Decimal("1.0"))
    1.0

    >>> decimal_encoder(Decimal("1"))
    1
    """
    if dec_value.as_tuple().exponent >= 0:  # type: ignore[operator]
        return int(dec_value)
    else:
        return float(dec_value)


ENCODERS_BY_TYPE: Dict[Type[Any], Callable[[Any], Any]] = {
    bytes: lambda o: o.decode(),
    Color: str,
    datetime.date: isoformat,
    datetime.datetime: isoformat,
    datetime.time: isoformat,
    datetime.timedelta: lambda td: td.total_
Skip to content
Follow FastAPI on LinkedIn to stay updated
logo
FastAPI
Development - Contributing

    en - English
    az - azərbaycan dili
    bn - বাংলা
    de - Deutsch
    es - español
    fa - فارسی
    fr - français
    he - עברית
    hu - magyar
    id - Bahasa Indonesia
    it - italiano
    ja - 日本語
    ko - 한국어
    nl - Nederlands
    pl - Polski
    pt - português
    ru - русский язык
    tr - Türkçe
    uk - українська мова
    ur - اردو
    vi - Tiếng Việt
    yo - Yorùbá
    zh - 简体中文
    zh-hant - 繁體中文
    😉

Type to start searching
fastapi/fastapi

    0.115.12
    84.4k
    7.3k

    FastAPI
    Features
    Learn
    Reference
    FastAPI People
    Resources
    About
    Release Notes

    Resources
        Help FastAPI - Get Help
        Development - Contributing
        Full Stack FastAPI Template
        External Links and Articles
        FastAPI and friends newsletter
        Repository Management Tasks

Table of contents

    Developing
        Virtual environment
        Install requirements using pip
        Using your local FastAPI
        Format the code
    Tests
    Docs
        Docs live
            Typer CLI (optional)
        Docs Structure
        Docs for tests
            Apps and docs at the same time
        Translations
            Tips and guidelines
            Existing language
            Don't Translate these Pages
            New Language
            Preview the result
            Translation specific tips and guidelines

    FastAPI
    Resources

Development - Contributing¶

First, you might want to see the basic ways to help FastAPI and get help.
Developing¶

If you already cloned the fastapi repository and you want to deep dive in the code, here are some guidelines to set up your environment.
Virtual environment¶

Follow the instructions to create and activate a virtual environment for the internal code of fastapi.
Install requirements using pip¶

After activating the environment, install the required packages:

pip install -r requirements.txt
████████████████████████████████████████ 100%
restart ↻

It will install all the dependencies and your local FastAPI in your local environment.
Using your local FastAPI¶

If you create a Python file that imports and uses FastAPI, and run it with the Python from your local environment, it will use your cloned local FastAPI source code.

And if you update that local FastAPI source code when you run that Python file again, it will use the fresh version of FastAPI you just edited.

That way, you don't have to "install" your local version to be able to test every change.

Technical Details

This only happens when you install using this included requirements.txt instead of running pip install fastapi directly.

That is because inside the requirements.txt file, the local version of FastAPI is marked to be installed in "editable" mode, with the -e option.
Format the code¶

There is a script that you can run that will format and clean all your code:

bash scripts/format.sh
restart ↻

It will also auto-sort all your imports.
Tests¶

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

bash scripts/test-cov-html.sh
restart ↻

This command generates a directory ./htmlcov/, if you open the file ./htmlcov/index.html in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.
Docs¶

First, make sure you set up your environment as described above, that will install all the requirements.
Docs live¶

During local development, there is a script that builds the site and checks for any changes, live-reloading:

python ./scripts/docs.py live
[INFO] Serving on http://127.0.0.1:8008
[INFO] Start watching changes
[INFO] Start detecting changes

restart ↻

It will serve the documentation on http://127.0.0.1:8008.

That way, you can edit the documentation/source files and see the changes live.

Tip

Alternatively, you can perform the same steps that scripts does manually.

Go into the language directory, for the main docs in English it's at docs/en/:

$ cd docs/en/

Then run mkdocs in that directory:

$ mkdocs serve --dev-addr 127.0.0.1:8008

Typer CLI (optional)¶

The instructions here show you how to use the script at ./scripts/docs.py with the python program directly.

But you can also use Typer CLI, and you will get autocompletion in your terminal for the commands after installing completion.

If you install Typer CLI, you can install completion with:

typer --install-completion
zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.

restart ↻

Docs Structure¶

The documentation uses MkDocs.

And there are extra tools/scripts in place to handle translations in ./scripts/docs.py.

Tip

You don't need to see the code in ./scripts/docs.py, you just use it in the command line.

All the documentation is in Markdown format in the directory ./docs/en/.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the ./docs_src/ directory.

And those Python files are included/injected in the documentation when generating the site.
Docs for tests¶

Most of the tests actually run against the example source files in the documentation.

This helps to make sure that:

    The documentation is up-to-date.
    The documentation examples can be run as is.
    Most of the features are covered by the documentation, ensured by test coverage.

Apps and docs at the same time¶

If you run the examples with, e.g.:

fastapi dev tutorial001.py
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

restart ↻

as Uvicorn by default will use the port 8000, the documentation on port 8008 won't clash.
Translations¶

Help with translations is VERY MUCH appreciated! And it can't be done without the help from the community. 🌎 🚀

Here are the steps to help with translations.
Tips and guidelines¶

    Check the currently existing pull requests for your language. You can filter the pull requests by the ones with the label for your language. For example, for Spanish, the label is lang-es.

    Review those pull requests, requesting changes or approving them. For the languages I don't speak, I'll wait for several others to review the translation before merging.

Tip

You can add comments with change suggestions to existing pull requests.

Check the docs about adding a pull request review to approve it or request changes.

    Check if there's a GitHub Discussion to coordinate translations for your language. You can subscribe to it, and when there's a new pull request to review, an automatic comment will be added to the discussion.

    If you translate pages, add a single pull request per page translated. That will make it much easier for others to review it.

    To check the 2-letter code for the language you want to translate, you can use the table List of ISO 639-1 codes.

Existing language¶

Let's say you want to translate a page for a language that already has translations for some pages, like Spanish.

In the case of Spanish, the 2-letter code is es. So, the directory for Spanish translations is located at docs/es/.

Tip

The main ("official") language is English, located at docs/en/.

Now run the live server for the docs in Spanish:

fast →
💬 Use the command "live" and pass the language code as a CLI argumentpython ./scripts/docs.py live es

Tip

Alternatively, you can perform the same steps that scripts does manually.

Go into the language directory, for the Spanish translations it's at docs/es/:

$ cd docs/es/

Then run mkdocs in that directory:

$ mkdocs serve --dev-addr 127.0.0.1:8008

Now you can go to http://127.0.0.1:8008 and see your changes live.

You will see that every language has all the pages. But some pages are not translated and have an info box at the top, about the missing translation.

Now let's say that you want to add a translation for the section Features.

    Copy the file at:

docs/en/docs/features.md

    Paste it in exactly the same location but for the language you want to translate, e.g.:

docs/es/docs/features.md

Tip

Notice that the only change in the path and file name is the language code, from en to es.

If you go to your browser you will see that now the docs show your new section (the info box at the top is gone). 🎉

Now you can translate it all and see how it looks as you save the file.
Don't Translate these Pages¶

🚨 Don't translate:

    Files under reference/
    release-notes.md
    fastapi-people.md
    external-links.md
    newsletter.md
    management-tasks.md
    management.md
    contributing.md

Some of these files are updated very frequently and a translation would always be behind, or they include the main content from English source files, etc.
New Language¶

Let's say that you want to add translations for a language that is not yet translated, not even some pages.

Let's say you want to add translations for Creole, and it's not yet there in the docs.

Checking the link from above, the code for "Creole" is ht.

The next step is to run the script to generate a new translation directory:




Now you can check in your code editor the newly created directory docs/ht/.

That command created a file docs/ht/mkdocs.yml with a simple config that inherits everything from the en version:

INHERIT: ../en/mkdocs.yml

Tip

You could also simply create that file with those contents manually.

That command also created a dummy file docs/ht/index.md for the main page, you can start by translating that one.

You can continue with the previous instructions for an "Existing Language" for that process.

You can make the first pull request with those two files, docs/ht/mkdocs.yml and docs/ht/index.md. 🎉
Preview the result¶

As already mentioned above, you can use the ./scripts/docs.py with the live command to preview the results (or mkdocs serve).

Once you are done, you can also test it all as it would look online, including all the other languages.

To do that, first build all the docs:






This builds all those independent MkDocs sites for each language, combines them, and generates the final output at ./site/.

Then you can serve that with the command serve:







Translation specific tips and guidelines¶

    Translate only the Markdown documents (.md). Do not translate the code examples at ./docs_src.

    In code blocks within the Markdown document, translate comments (# a comment), but leave the rest unchanged.

    Do not change anything enclosed in "``" (inline code).

    In lines starting with /// translate only the text part after |. Leave the rest unchanged.

    You can translate info boxes like /// warning with for example /// warning | Achtung. But do not change the word immediately after the ///, it determines the color of the info box.

    Do not change the paths in links to images, code files, Markdown documents.

    However, when a Markdown document is translated, the #hash-parts in links to its headings may change. Update these links if possible.
        Search for such links in the translated document using the regex #[^# ].
        Search in all documents already translated into your language for your-translated-document.md. For example VS Code has an option "Edit" -> "Find in Files".
        When translating a document, do not "pre-translate" #hash-parts that link to headings in untranslated documents.

Was this page helpful?
Previous
Help FastAPI - Get Help
Next
Full Stack FastAPI Template
The FastAPI trademark is owned by @tiangolo and is registered in the US and across other regions
Made with Material for MkDocs
seconds(),
    Decimal: decimal_encoder,
    Enum: lambda o: o.value,
    frozenset: list,
    deque: list,
    GeneratorType: list,
    IPv4Address: str,
    IPv4Interface: str,
    IPv4Network: str,
    IPv6Address: str,
    IPv6Interface: str,
    IPv6Network: str,
    NameEmail: str,
    Path: str,
    Pattern: lambda o: o.pattern,
    SecretBytes: str,
    SecretStr: str,
    set: list,
    UUID: str,
    Url: str,
    AnyUrl: str,
}


def generate_encoders_by_class_tuples(
    type_encoder_map: Dict[Any, Callable[[Any], Any]],
) -> Dict[Callable[[Any], Any], Tuple[Any, ...]]:
    encoders_by_class_tuples: Dict[Callable[[Any], Any], Tuple[Any, ...]] = defaultdict(
        tuple
    )
    for type_, encoder in type_encoder_map.items():
        encoders_by_class_tuples[encoder] += (type_,)
    return encoders_by_class_tuples


encoders_by_class_tuples = generate_encoders_by_class_tuples(ENCODERS_BY_TYPE)



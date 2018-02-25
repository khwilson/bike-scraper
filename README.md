# Bike Scraper

This is a simple little script for pulling data periodically
from all the local DC bike share APIs.

## Requirements

You need python 3.6 because I like f-strings.

## Usage

This is mean to be used with a postgres database. First you'll need
to fill in the `config.yml`.

After doing that, install the software (we recommend a virtualenv):

```bash
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Then create the relevant tables

```bash
bikecli create config.yml
```

And then get data!

```bash
bikecli pull config.yml jump lime ofo spin
```

## Limitations

Mobike is also in the District, but as of yet does not have a public API.

## License

MIT

import logging

import click
import yaml

from . import database as db
from . import puller


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')


@click.group()
def cli():
  pass


@cli.command('create')
@click.argument('config')
def create_command(config):
  with open(config) as f:
    config = yaml.load(f)
  click.echo("Creating table {}".format(db.TABLE_NAME))
  conn = db.get_connection(config['db'])
  curs = conn.cursor()
  db.create_table(curs)
  curs.close()
  conn.commit()
  conn.close()
  click.echo("Done creating table")


@cli.command('pull')
@click.argument('config')
@click.argument('providers', nargs=-1, type=click.Choice(['jump', 'lime', 'ofo', 'spin']))
def pull_command(config, providers):
  with open(config) as f:
    config = yaml.load(f)
  conn = db.get_connection(config['db'])
  curs = conn.cursor()
  click.echo("Pulling data for {} provider".format(len(providers)))
  for provider in providers:
    click.echo("Pulling data for {}".format(provider))
    try:
      positions = puller.for_provider(provider)()
      db.insert_positions(curs, provider, positions)
    except puller.SomethingWrongError as exc:
      click.echo("Something went wrong pulling for {}: {}".format(provider, exc))

  curs.close()
  conn.commit()
  conn.close()


if __name__ == '__main__':
  cli()

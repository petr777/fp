#!/usr/bin/python3
import click
import json
from engine.fogsoft.scraper_table_lots import start

with open('data.json', "r") as f:
    trading_platform = json.load(f)

@click.command()
@click.option('--platform', '-p',
              help='Choose a platform for parsing',
              type=click.Choice(trading_platform.keys()))
@click.option('--slow_mo', '-s', type=int, default=500)
@click.option('--limit_page', '-l', type=int, default=10)
def choose_platform(platform, slow_mo, limit_page):
    print('-------------------------------')
    click.echo(f"Selected platform:".ljust(19) + platform)
    click.echo(f"Slow mo:".ljust(19) + str(slow_mo))
    click.echo(f"Limit page:".ljust(19) + str(limit_page))
    print('-------------------------------')
    start_url = trading_platform[platform]['start_url']
    start(platform, start_url, slow_mo, limit_page)


if __name__ == '__main__':
    choose_platform()

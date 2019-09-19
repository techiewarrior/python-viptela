import click
from .show import show
from .export import export
from .import_cmd import import_cmd
from cisco_sdwan import vmanage

class CatchAllExceptions(click.Group):

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as exc:
            click.secho('Exception raised while running your command', fg="red")
            click.secho("Please open an issue and provide this info:", fg="red")
            click.secho("%s" % exc, fg="red")

class Vmanage(object):
    def __init__(self, host=None, user=None, password=None):
        self.host = host
        self.user = user
        self.password = password

# @click.group(cls=CatchAllExceptions)
@click.group()
@click.option('--host', envvar='VMANAGE_HOST', help='vManage Host (env: VMANAGE_HOST)', required=True)
@click.option('--user', envvar='VMANAGE_USER', help='vManage Username (env: VMANAGE_USER)', required=True)
@click.option('--password', envvar='VMANAGE_PASSWORD', prompt=True, hide_input=True, help='vManage Password (env: VMANAGE_PASSWORD)', required=True)
@click.pass_context
def vmanage_cli(ctx, host, user, password):

    ctx.obj = vmanage.vmanage_session(host=host, user=user, password=password)

vmanage_cli.add_command(show)
vmanage_cli.add_command(export)
vmanage_cli.add_command(import_cmd)

if __name__ == '__main__':
    vmanage_cli()  # pragma: no cover
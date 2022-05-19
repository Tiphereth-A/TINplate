"""From: <https://github.com/pallets/click/tree/main/examples/aliases>
"""
import click
import yaml


class AliasConfig:
    """Only holds aliases"""

    def __init__(self):
        self.aliases: dict = {}

    def add_alias(self, alias: str, cmd: str):
        self.aliases.update({alias: cmd})
        return self

    def read_config(self, filepath: str):
        with open(filepath, 'r', encoding='utf8') as f:
            self.aliases.update(yaml.safe_load(f))

    def write_config(self, filepath: str):
        with open(filepath, 'w', encoding='utf8') as f:
            yaml.dump(self.aliases, f)


pass_config = click.make_pass_decorator(AliasConfig, ensure=True)


class AliasedGroup(click.Group):
    """This subclass of a group supports looking up aliases in a config
    file and with a bit of magic.
    """

    def get_command(self, ctx: click.Context, cmd_name: str):
        # Step one: bulitin commands as normal
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Step two: find the config object and ensure it's there.  This
        # will create the config object is missing.
        cfg = ctx.ensure_object(AliasConfig)

        # Step three: look up an explicit command alias in the config
        if cmd_name in cfg.aliases:
            actual_cmd = cfg.aliases[cmd_name]
            return click.Group.get_command(self, ctx, actual_cmd)

        # Alternative option: if we did not find an explicit alias we
        # allow automatic abbreviation of the command.  "status" for
        # instance will match "st".  We only allow that however if
        # there is only one command.
        matches: list[str] = [x for x in self.list_commands(ctx) if x.lower().startswith(cmd_name.lower())]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx: click.Context, args: list[str]):
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

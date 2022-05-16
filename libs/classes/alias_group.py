import click


# From: <https://stackoverflow.com/questions/46641928/python-click-multiple-command-names>
class AliasGroup(click.Group):

    def command(self, *args, **kwargs):
        """
        Behaves the same as `click.Group.command()` except if passed
        a list of names, all after the first will be aliases for the first.
        """

        def decorator(f):
            if isinstance(args[0], list):
                _args = [args[0][0]] + list(args[1:])
                for alias in args[0][1:]:
                    cmd = super(AliasGroup, self).command(alias, *args[1:], **kwargs)(f)
                    cmd.short_help = f"*Alias for '{_args[0]}'*"
            else:
                _args = args
            cmd = super(AliasGroup, self).command(*_args, **kwargs)(f)
            return cmd

        return decorator

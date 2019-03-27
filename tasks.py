"""Using `invoke` to start tests and and other commandline tools.
"""

from invoke import run, task


@task
def test(ctx):
    """Run standard tests.


    Usage (commandline): inv test
    """
    # run('py.test --assert=reinterp', pty=True)
    run('py.test', pty=True)
    # run('py.test --assert=plain', pty=True)

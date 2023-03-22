from invoke import task

@task
def run(ctx):
    ctx.run("cd app && flask run", pty=True)

@task
def lint(ctx):
    ctx.run("pylint app", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive app", pty=True)

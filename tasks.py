from invoke import task

@task
def validate(ctx):
    ctx.run('pylint secretctl/')
    ctx.run('coverage run --source=secretctl/ setup.py test')
    ctx.run('coverage report')

AKIAZXAHKKQAN2YA3MOZ

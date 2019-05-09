from invoke import task
import multiprocessing
import sys
import toml

pty = sys.stdout.isatty()


def get_package_name() -> str:
    pyproject = toml.load(open('pyproject.toml', 'r'))
    return pyproject['tool']['poetry']['name']


@task
def lint(c):
    package_name = get_package_name()
    nproc = multiprocessing.cpu_count()
    c.run(f'mypy {package_name}.py tests', echo=True, pty=pty)
    c.run(f'pylint --jobs {nproc} {package_name} tests', echo=True, pty=pty)
    c.run(f'pydocstyle {package_name} tests', echo=True, pty=pty)


@task
def test(c):
    package_name = get_package_name()
    c.run(
        f'pytest --cov={package_name} --doctest-modules --ignore=docs --ignore=tasks.py',
        echo=True,
        pty=pty)


@task
def html(c):
    c.run('make -C docs html', echo=True, pty=pty)


@task
def serve(c):
    c.run('sphinx-autobuild docs docs/_build/html --host 0.0.0.0 --watch .',
          echo=True,
          pty=pty)

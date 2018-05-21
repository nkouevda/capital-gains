from setuptools import setup

version = {}

with open('capital_gains/__version__.py', 'r') as f:
  exec(f.read(), version)

with open('README.md', 'r') as f:
  readme = f.read()

setup(
    name='capital-gains',
    version=version['__version__'],
    description='Capital gains calculator',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/nkouevda/capital-gains',
    author='Nikita Kouevda',
    author_email='nkouevda@gmail.com',
    license='MIT',
    packages=['capital_gains'],
    entry_points={
        'console_scripts': [
            'capital-gains=capital_gains.capital_gains:main',
        ],
    },
)

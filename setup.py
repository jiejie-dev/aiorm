from setuptools import setup, find_packages

setup(
    name='nory',
    version='1',
    description='A simple web framework using asyncio',
    url='http://github.com/jeremaihloo/nory',
    author='jeremaihloo',
    author_email='jeremaihloo1024@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    zip_safe=False,
    entry_points={
        'console_scripts': ['nory=nory.hotting:main'],
    }
)

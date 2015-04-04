"""
Slacky
------

A Python package for Slack's JSON REST API.

Slacky is Simple
````````````````

Save in a hello.py:

.. code:: python

    from slacky import Slacky
    slacky = Slacky(token='<Your slack api token>')

    slacky.chat.post_message('#general', 'Hello World!!')

    # '#' is not necessary with channel name.
    slacky.chat.post_message('general', 'Hello World!!')

And Easy to Setup
`````````````````

And run it:

.. code:: bash

    $ pip install slacky
    $ python hello.py

Links
`````

* `website <https://github.com/nabetama/slacky>`_

"""
from setuptools import setup

setup(
    name='slacky',
    version="0.1.4",
    description="Package for Slack's API",
    long_description=__doc__,
    author='Mao Nabeta',
    author_email='mao.nabeta@gmail.com',
    url='https://github.com/nabetama/slacky',
    packages=['slacky'],
    install_requires=['requests', 'six'],
    provides=['slack'],
    keywords='slack',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )

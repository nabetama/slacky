from setuptools import setup

setup(
    name='slacky',
    version="0.1.2",
    description="Package for Slack's API",
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

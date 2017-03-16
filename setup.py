from setuptools import setup

setup(
    name='make-podcast',
    version='1.0.0',
    description='Generate podcast XML from a directory of MP3 files',
    url='https://github.com/williamjacksn/make_podcast',
    author='William Jackson',
    author_email='william@subtlecoolness.com',
    py_modules=['make_podcast'],
    install_requires=['mutagen'],
    entry_points={
        'console_scripts': [
            'make_podcast = make_podcast:main'
        ]
    }
)

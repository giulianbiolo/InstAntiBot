import setuptools
from pathlib import Path

setuptools.setup(
    name="igramscraper",
    version="0.3.5",
    description=('scrapes medias, likes, followers, tags and all metadata'),
#     long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="MIT",
    maintainer="realsirjoe, leungwaiban",
    author='realsirjoe, leungwaiban',
    url='https://github.com/realsirjoe/instagram-scraper',
    install_requires=[
        'requests>=2.21.0',
        'python-slugify==3.0.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)

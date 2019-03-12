import os
import pathlib
import requests
import sys
import urllib.parse
import xml.etree.ElementTree


def version() -> str:
    """Read version from Dockerfile"""
    dockerfile = pathlib.Path(__file__).resolve().parent / 'Dockerfile'
    with open(dockerfile) as f:
        for line in f:
            if 'org.label-schema.version' in line:
                return line.strip().split('=', maxsplit=1)[1]
    return 'unknown'


def main():
    print(f'download-podcast {version()}')
    podcast_url = os.getenv('PODCAST_URL')
    if podcast_url is None:
        print('Please set PODCAST_URL')
        sys.exit(1)
    print(f'PODCAST_URL is {podcast_url}')
    response = requests.get(podcast_url)
    print(f'Response encoding is {response.encoding}')
    text = response.text
    root = xml.etree.ElementTree.fromstring(text)
    channel = root.find('channel')
    items = channel.findall('item')
    working_dir = pathlib.Path().resolve()
    for item in items:
        title = item.find('title')
        guid = item.find('guid')
        enclosure = item.find('enclosure')
        url = enclosure.get('url')
        parsed_url = urllib.parse.urlparse(url)
        print(f'Downloading from: {url}')
        source_path = pathlib.Path(parsed_url.path)
        target_path = working_dir / source_path.name
        print(f'Saving to {target_path}')
        with target_path.open('wb') as f:
            source = requests.get(url)
            f.write(source.content)


if __name__ == '__main__':
    main()

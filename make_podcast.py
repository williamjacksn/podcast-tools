import argparse
import datetime
import json
import mutagen.id3
import mutagen.mp3
import pathlib
import uuid
import xml.etree.ElementTree as ETree


def get_pub_date(index):
    date = datetime.date(2016, 1, 1) + datetime.timedelta(days=index)
    return f'{date:%a}, {date.day} {date:%b %Y} 08:00:00 +0000'


def make_podcast_xml(podcast_info):
    rss_attrib = {'version': '2.0', 'xmlns:atom': 'http://www.w3.org/2005/Atom',
                  'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    rss = ETree.Element('rss', attrib=rss_attrib)
    rss.text = '\n  '
    rss.tail = '\n'
    channel = ETree.SubElement(rss, 'channel')
    channel.text = '\n    '
    channel.tail = '\n'
    base_url = podcast_info['base_url']
    link_self = ETree.SubElement(channel, 'atom:link', href=f'{base_url}_.xml', rel='self')
    link_self.tail = '\n    '
    language = ETree.SubElement(channel, 'language')
    language.text = 'en-us'
    language.tail = '\n    '
    title = ETree.SubElement(channel, 'title')
    title.text = podcast_info['title']
    title.tail = '\n    '
    author = ETree.SubElement(channel, 'itunes:author')
    author.text = podcast_info['author']
    author.tail = '\n    '
    image = ETree.SubElement(channel, 'itunes:image', href=f'{base_url}_.jpg')
    image.tail = '\n    '
    link = ETree.SubElement(channel, 'link')
    link.text = podcast_info['base_url']
    link.tail = '\n    '
    description = ETree.SubElement(channel, 'description')
    description.text = podcast_info['description']
    description.tail = '\n    '
    category = ETree.SubElement(channel, 'itunes:category', text='Arts')
    category.text = '\n      '
    category.tail = '\n    '
    sub_category = ETree.SubElement(category, 'itunes:category', text='Literature')
    sub_category.tail = '\n    '
    owner = ETree.SubElement(channel, 'itunes:owner')
    owner.text = '\n      '
    owner.tail = '\n    '
    email = ETree.SubElement(owner, 'itunes:email')
    email.text = podcast_info['owner_email']
    email.tail = '\n    '
    explicit = ETree.SubElement(channel, 'itunes:explicit')
    explicit.text = 'no'
    explicit.tail = '\n    '
    block = ETree.SubElement(channel, 'itunes:block')
    block.text = 'yes'
    block.tail = '\n    '
    return rss


def add_item_to_podcast(rss, podcast_info, mp3_info, index):
    channel = rss.find('channel')
    item = ETree.SubElement(channel, 'item')
    item.text = '\n      '
    item.tail = '\n    '
    title = ETree.SubElement(item, 'title')
    title.text = mp3_info['title']
    title.tail = '\n      '
    base_url = podcast_info['base_url']
    item_name = mp3_info['name']
    length = str(mp3_info['size'])
    enclosure = ETree.SubElement(item, 'enclosure', url=f'{base_url}{item_name}', type='audio/mpeg', length=length)
    enclosure.tail = '\n      '
    guid = ETree.SubElement(item, 'guid', isPermaLink='false')
    guid.text = str(uuid.uuid4())
    guid.tail = '\n      '
    pub_date = ETree.SubElement(item, 'pubDate')
    pub_date.text = get_pub_date(index)
    pub_date.tail = '\n      '
    duration = ETree.SubElement(item, 'itunes:duration')
    duration.text = mp3_info['duration']
    duration.tail = '\n    '


def duration_string(num_seconds):
    hours = minutes = 0
    if num_seconds < 60:
        seconds = num_seconds
    else:
        seconds = num_seconds % 60
        minutes = num_seconds // 60
        if minutes < 60:
            pass
        else:
            hours = minutes // 60
            minutes %= 60
    return f'{hours}:{minutes:02d}:{seconds:02d}'


def get_mp3s(path):
    if isinstance(path, pathlib.Path):
        p = path.resolve()
    else:
        p = pathlib.Path(path).resolve()
    if p.is_dir():
        for item in p.iterdir():
            if item.suffix.lower() == '.mp3':
                yield item


def get_file_info(mp3: pathlib.Path):
    info = {'name': mp3.name}
    audio = mutagen.mp3.MP3(str(mp3))
    info['duration'] = duration_string(int(audio.info.length))
    info['size'] = mp3.stat().st_size
    id3 = mutagen.id3.ID3(str(mp3))
    info['title'] = id3.getall('TIT2')[0][0]
    return info


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    return parser.parse_args()


def main():
    args = parse_args()
    info = {'base_url': '', 'title': '', 'author': '', 'description': '', 'owner_email': ''}
    path = pathlib.Path(args.path).resolve()
    saved_info_path = path / 'podcast_info.json'
    if saved_info_path.exists():
        with saved_info_path.open() as f:
            info = json.load(f)
    info['base_url'] = input('Base url [{base_url}]: '.format(**info)) or info['base_url']
    info['title'] = input('Podcast title [{title}]: '.format(**info)) or info['title']
    info['author'] = input('Podcast author [{author}]: '.format(**info)) or info['author']
    info['description'] = input('Podcast description [{description}]: '.format(**info)) or info['description']
    info['owner_email'] = input('Podcast owner email [{owner_email}]: '.format(**info)) or info['owner_email']
    with saved_info_path.open('w') as f:
        json.dump(info, f, indent=2)

    rss = make_podcast_xml(info)

    for index, mp3 in enumerate(sorted(list(get_mp3s(args.path)))):
        add_item_to_podcast(rss, info, get_file_info(mp3), index)

    tree = ETree.ElementTree(rss)
    tree.write(path / '_.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    main()

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
    return '{0:%a}, {0.day} {0:%b %Y} 08:00:00 +0000'.format(date)


def make_podcast_xml(podcast_info):
    rss = ETree.Element('rss')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
    rss.set('version', '2.0')
    channel = ETree.SubElement(rss, 'channel')
    link_self = ETree.SubElement(channel, 'atom:link')
    link_self.set('href', '{base_url}_.xml'.format(**podcast_info))
    link_self.set('rel', 'self')
    language = ETree.SubElement(channel, 'language')
    language.text = 'en-us'
    title = ETree.SubElement(channel, 'title')
    title.text = podcast_info['title']
    author = ETree.SubElement(channel, 'itunes:author')
    author.text = podcast_info['author']
    image = ETree.SubElement(channel, 'itunes:image')
    image.set('href', '{base_url}_.jpg'.format(**podcast_info))
    link = ETree.SubElement(channel, 'link')
    link.text = podcast_info['base_url']
    description = ETree.SubElement(channel, 'description')
    description.text = podcast_info['description']
    category = ETree.SubElement(channel, 'itunes:category')
    category.set('text', 'Arts')
    sub_category = ETree.SubElement(category, 'itunes:category')
    sub_category.set('text', 'Literature')
    owner = ETree.SubElement(channel, 'itunes:owner')
    email = ETree.SubElement(owner, 'itunes:email')
    email.text = podcast_info['owner_email']
    explicit = ETree.SubElement(channel, 'itunes:explicit')
    explicit.text = 'no'
    return rss


def add_item_to_podcast(rss, podcast_info, mp3_info, index):
    channel = rss.find('channel')
    item = ETree.SubElement(channel, 'item')
    title = ETree.SubElement(item, 'title')
    title.text = mp3_info['title']
    enclosure = ETree.SubElement(item, 'enclosure')
    enclosure.set('url', '{}{}'.format(podcast_info['base_url'], mp3_info['name']))
    enclosure.set('length', str(mp3_info['size']))
    enclosure.set('type', 'audio/mpeg')
    guid = ETree.SubElement(item, 'guid')
    guid.set('isPermaLink', 'false')
    guid.text = str(uuid.uuid4())
    pub_date = ETree.SubElement(item, 'pubDate')
    pub_date.text = get_pub_date(index)
    duration = ETree.SubElement(item, 'itunes:duration')
    duration.text = mp3_info['duration']


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
    return '{}:{:02d}:{:02d}'.format(hours, minutes, seconds)


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

    print(ETree.tostring(rss, encoding='unicode'))

if __name__ == '__main__':
    main()

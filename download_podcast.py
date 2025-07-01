import httpx
import os
import pathlib
import sys
import urllib.parse
import xml.etree.ElementTree


def main():
    podcast_url = os.getenv("PODCAST_URL")
    if podcast_url is None:
        print("Please set PODCAST_URL")
        sys.exit(1)
    print(f"PODCAST_URL is {podcast_url}")
    response = httpx.get(podcast_url)
    print(f"Response encoding is {response.encoding}")
    text = response.text
    root = xml.etree.ElementTree.fromstring(text)
    channel = root.find("channel")
    items = channel.findall("item")
    working_dir = pathlib.Path().resolve()
    for item in items:
        enclosure = item.find("enclosure")
        url = enclosure.get("url")
        parsed_url = urllib.parse.urlparse(url)
        print(f"Downloading from: {url}")
        source_path = pathlib.Path(parsed_url.path)
        target_path = working_dir / source_path.name
        print(f"Saving to {target_path}")
        with target_path.open("wb") as f:
            source = httpx.get(url)
            f.write(source.content)


if __name__ == "__main__":
    main()

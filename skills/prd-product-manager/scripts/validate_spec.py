#!/usr/bin/env python3
"""Validate structural delivery requirements; business and screenshot review remain manual."""
import argparse
import base64
import re
from html.parser import HTMLParser
from pathlib import Path

class SpecParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.anchors = []
        self.images = 0
        self.features = []
        self.current = None
        self.errors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'article' and 'feature' in a.get('class', '').split():
            self.current = {'id': a.get('id', ''), 'images': 0, 'text': ''}
            self.features.append(self.current)
        if tag == 'a' and a.get('href', '').startswith('#'):
            self.anchors.append(a['href'][1:])
        if tag in ('script', 'link') and (a.get('src') or a.get('href')):
            self.errors.append('External script/style resource: ' + tag)
        if tag != 'img':
            return
        if a.get('id') == 'zoom-image' and not a.get('src'):
            return
        self.images += 1
        if self.current is not None:
            self.current['images'] += 1
        match = re.fullmatch(r'data:image/(png|jpeg|jpg|webp|gif|svg\+xml);base64,([A-Za-z0-9+/=\s]+)', a.get('src', ''))
        if not match:
            self.errors.append('Image must be an embedded base64 data URI')
            return
        try:
            data = base64.b64decode(re.sub(r'\s', '', match[2]), validate=True)
            kind = match[1]
            valid = {'png': data.startswith(b'\x89PNG\r\n\x1a\n'),
                     'jpeg': data.startswith(b'\xff\xd8'), 'jpg': data.startswith(b'\xff\xd8'),
                     'gif': data.startswith((b'GIF87a', b'GIF89a')),
                     'webp': data[:4] == b'RIFF' and data[8:12] == b'WEBP',
                     'svg+xml': b'<svg' in data}[kind]
            if not valid:
                raise ValueError('image signature')
        except (ValueError, KeyError):
            self.errors.append('Invalid base64 image or image signature')

    def handle_endtag(self, tag):
        if tag == 'article':
            self.current = None

    def handle_data(self, data):
        if self.current is not None:
            self.current['text'] += data


def validate(path):
    content = path.read_text(encoding='utf-8')
    parser = SpecParser()
    parser.feed(content)
    errors = parser.errors
    ids = parser.ids
    if len(ids) != len(set(ids)):
        errors.append('Duplicate element IDs')
    for target in parser.anchors:
        if target and target not in ids:
            errors.append('Missing anchor: ' + target)
    required = ['revision', 'requirements', 'functions', 'states', 'permissions', 'limits', 'nonfunctional', 'handoff']
    if any(id not in ids for id in required):
        errors.append('Missing required chapter IDs')
    elif [ids.index(id) for id in required] != sorted(ids.index(id) for id in required):
        errors.append('Chapter order mismatch')
    if 'contracts' not in ids:
        errors.append('Missing contracts section (state not applicable when appropriate)')
    if not parser.features:
        errors.append('No feature articles')
    for feature in parser.features:
        if not feature['id'] or not feature['images'] or 'AC-' + feature['id'] not in feature['text']:
            errors.append('Missing ID, screenshot or acceptance marker: ' + feature['id'])
    without_comments = re.sub(r'<!--.*?-->', '', content, flags=re.S)
    if re.search(r'\{\{[A-Z_]+\}\}|\[插入截图\]', without_comments):
        errors.append('Unresolved template placeholders')
    if re.search(r'(?:url\(|@import\s)[^;}]*https?://', content):
        errors.append('Remote CSS resource dependency')
    return errors, len(parser.features), parser.images

if __name__ == '__main__':
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('file', type=Path)
    options = args.parse_args()
    errors, features, images = validate(options.file)
    for error in errors:
        print('FAIL:', error)
    if not errors:
        print(f'PASS: {features} features, {images} embedded images; visual and business review still required.')
    raise SystemExit(bool(errors))

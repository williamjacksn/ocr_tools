import argparse
import mutagen.id3
import rainwave_tools.utils


def log(m):
    print(m)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('old_name')
    parser.add_argument('new_name')
    parser.add_argument('path', nargs='*', default='.')
    return parser.parse_args()


def main():
    args = parse_args()
    change_count = 0

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        changed = False
        tags = mutagen.id3.ID3(str(mp3))
        artist_tag = tags.getall('TPE1')[0].text[0]
        artists = [a.strip() for a in artist_tag.split(',')]
        for i, artist in enumerate(artists):
            if artist == args.old_name:
                artists[i] = args.new_name
                changed = True
        if changed:
            change_count += 1
            artist_tag = ', '.join(artists)
            tags.delall('TPE1')
            tags.add(mutagen.id3.TPE1(encoding=3, text=[artist_tag]))
            tags.save()
            log('{} : new artist tag {!r}'.format(mp3, artist_tag))

    m = '** updated tags in {} file'.format(change_count)
    if change_count != 1:
        m = '{}s'.format(m)
    log(m)

if __name__ == '__main__':
    main()
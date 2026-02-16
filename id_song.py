import asyncio
import os
import urllib.request

import eyed3
import eyed3.plugins.art

from shazamio import Shazam, Serialize

MUSIC_FOLDER = "/Users/diegocarvalho/Music/Music/Media.localized/Music/Unknown"


async def main():
    shazam = Shazam()
    for root, _dirs, files in os.walk(MUSIC_FOLDER):
        for file in files:
            path = os.path.join(root, file)
            if not path.lower().endswith(".mp3"):
                continue
            print(path)

            # Identify song using Shazam
            out = await shazam.recognize(path)
            if len(out['matches']) < 1:
                print("Shazam could not find a match")
                continue
            data = Serialize.track(out['track'])

            # Extract data from Shazam response (use .get() for optional fields)
            track = out['track']
            tags = {}
            tags['title'] = track.get('title', '')
            tags['artist'] = track.get('subtitle', '')
            tags['genre'] = (track.get('genres') or {}).get('primary', '')
            tags['album'] = ""
            tags['year'] = ""

            cover_art = (track.get('images') or {}).get('coverarthq')
            if cover_art:
                cover_art = cover_art.replace("400x400", "1000x1000")

            for section in data.sections:
                if section.type == "SONG":
                    for md in section.metadata:
                        if md.title == "Album":
                            tags['album'] = md.text
                        if md.title == "Released":
                            tags['year'] = md.text

            print("Shazam: " + tags['artist'] + " - " + tags['title'] + " (" + tags['album'] + ")" if tags['album'] else "Shazam: " + tags['artist'] + " - " + tags['title'])

            # Reset current tags
            id3 = eyed3.load(path)
            if id3.tag:
                id3.tag.clear()
                id3.tag.save()
            else:
                id3.initTag()
                id3.tag.save()

            # Save new tags
            id3 = eyed3.load(path)
            id3.tag.album = tags['album']
            id3.tag.artist = tags['artist']
            id3.tag.album_artist = tags['artist']
            id3.tag.genre = tags['genre']
            id3.tag.title = tags['title']
            id3.tag.year = tags['year']

            # Download art and (temporary) save locally (same dir as the MP3)
            if cover_art:
                local_art = os.path.join(root, "tmp_file" + cover_art[-4:])
                try:
                    urllib.request.urlretrieve(cover_art, local_art)

                    # Save art to MP3 file
                    id3_front_cover_id = eyed3.utils.art.TO_ID3_ART_TYPES['FRONT_COVER'][0]
                    id3_cover = eyed3.plugins.art.ArtFile(local_art)
                    id3_cover.id3_art_type = id3_front_cover_id
                    id3.tag.images.set(id3_cover.id3_art_type, id3_cover.image_data, id3_cover.mime_type)

                    # Save the new tags
                    id3.tag.save(version=(2, 3, 0))

                    print("Saved new tags")
                finally:
                    if os.path.isfile(local_art):
                        os.remove(local_art)
            else:
                id3.tag.save(version=(2, 3, 0))
                print("Saved new tags (no cover art)")

if __name__ == "__main__":
    asyncio.run(main())

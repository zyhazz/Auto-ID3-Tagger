# Auto ID3 Tagger
This script will read all files in the provided folder (MUSIC_FOLDER) and identify the songs using Shazam.
It will then collect some information about the songs, including album art, and write this information to the ID3 tags
of the MP3 file.

### Requirements
- **Python 3.12 or 3.13** (3.14 is not yet supported due to a compatibility issue with shazamio-core.)

### Setup
```bash
python3.13 -m venv venv
source venv/bin/activate   # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run
```bash
# Edit MUSIC_FOLDER in id_song.py, then:
python id_song.py
```

### Packages used
[ShazamIO](https://github.com/dotX12/ShazamIO) - Used to identify the songs

[EyeD3](https://eyed3.readthedocs.io/en/latest/index.html) - Used to write the ID3 tags
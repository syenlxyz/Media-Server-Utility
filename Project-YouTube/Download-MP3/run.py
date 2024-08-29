from alive_progress import alive_it
from datetime import datetime
from pathlib import Path
from pytube import YouTube, Playlist
from urllib.parse import urlparse, parse_qs
import subprocess

def run():
    input_path = Path.cwd() / 'input'
    output_path = Path.cwd() / 'output'
    
    if not input_path.is_dir():
        input_path.mkdir()
    
    if not output_path.is_dir():
        output_path.mkdir()
    
    options = {
        'length': 70,
        'spinner': 'classic',
        'bar': 'classic2',
        'receipt_text': True,
        'dual_line': True
    }
    
    playlist = get_playlist()
    if not playlist:
        return None
    
    results = alive_it(
        playlist,
        len(playlist),
        finalize=lambda bar: bar.text('Downloading MP3: done'),
        **options
    )
    
    for url in results:
        results.text(f'Downloading MP3: {url}')
        yt = YouTube(url)
        input_file = Path(
            yt.streams
            .filter(only_audio=True)
            .order_by('bitrate')
            .desc()
            .first()
            .download(input_path)
        )
        output_file = output_path / f'{input_file.stem}.mp3'
        subprocess.run(f'ffmpeg -i "{input_file}" -y "{output_file}"')

def get_playlist():
    playlist = []
    while True:
        url = input('Paste link here (or press ENTER to continue): ')
        if not url:
            break
        result = urlparse(url)
        netloc = result.netloc
        if 'youtu.be' == netloc:
            playlist.append(url)
        elif 'youtube.com' in netloc:
            query = result.query
            params = parse_qs(query)
            keys = list(params.keys())
            if 'list' in keys:
                p = Playlist(url)
                playlist.extend(p.video_urls)
            elif 'v' in keys:
                playlist.append(url)
            else:
                print('Invalid URL. Please try again.')
        else:
            print('Invalid URL. Please try again.')
    return playlist

if __name__ == '__main__':
    print(f'Running {Path(__file__).parent.name}')
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    run_time = end_time - start_time
    print(f'Execution time: {run_time}')
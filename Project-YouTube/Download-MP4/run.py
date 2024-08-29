from alive_progress import alive_it
from datetime import datetime
from pathlib import Path
from pytube import YouTube, Playlist
from urllib.parse import urlparse, parse_qs

def run():
    output_path = Path.cwd() / 'output'
    if not output_path.is_dir():
        output_path.mkdir()
    
    options = {
        'length': 70,
        'spinner': 'classic',
        'bar': 'classic2',
        'receipt_text': True,
        'dual_line': True
    }
    
    url_list = get_url_list()
    results = alive_it(
        url_list,
        len(url_list),
        finalize=lambda bar: bar.text('Downloading MP4: done'),
        **options
    )
    
    for url in results:
        results.text(f'Downloading MP4: {url}')
        yt = YouTube(url)
        yt.streams \
        .filter(progressive=True) \
        .first() \
        .download(output_path)

def get_url_list():
    url = input('Paste link here: ')
    while not url:
        result = urlparse(url)
        netloc = result.netloc
        if 'youtu.be' == netloc:
            url_list = [url]
            return url_list
        elif 'youtube.com' in netloc:
            query = result.query
            params = parse_qs(query)
            keys = list(params.keys())
            if 'list' in keys:
                p = Playlist(url)
                url_list = list(p.video_urls)
                return url_list
            elif 'v' in keys:
                url_list = [url]
                return url_list
            else:
                url = input('Invalid URL. Please try again: ')
        else:
            url = input('Invalid URL. Please try again: ')

if __name__ == '__main__':
    print(f'Running {Path(__file__).parent.name}')
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    run_time = end_time - start_time
    print(f'Execution time: {run_time}')
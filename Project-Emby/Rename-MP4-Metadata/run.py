from alive_progress import alive_it
from datetime import datetime
from mutagen import File
from pathlib import Path

def run():
    input_path = Path.cwd() / 'input'
    if not input_path.is_dir():
        input_path.mkdir()
    
    options = {
        'length': 70,
        'spinner': 'classic',
        'bar': 'classic2',
        'receipt_text': True,
        'dual_line': True
    }
    
    file_list = list(input_path.glob('**/*.mp4'))
    results = alive_it(
        file_list,
        len(file_list),
        finalize=lambda bar: bar.text('Renaming MP4 metadata: done'),
        **options
    )
    
    for file_path in results:
        results.text(f'Renaming MP4 metadata: {file_path.name}')
        file = File(file_path, easy=True)
        file['title'] = file_path.stem
        file['comment'] = file_path.stem
        file.save()

if __name__ == '__main__':
    print(f'Running {Path(__file__).parent.name}')
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    run_time = end_time - start_time
    print(f'Execution time: {run_time}')
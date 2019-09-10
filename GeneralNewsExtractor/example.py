import json
import glob
from gne import GeneralNewsExtractor


if __name__ == '__main__':
    html_list = glob.glob('**/*.html', recursive=True)
    for html_file in html_list:
        with open(html_file, encoding='utf-8') as f:
            html = f.read()
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
        print(f'>>>>>>>>>>>>>{html_file}>>>>>>>>>>>>>')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

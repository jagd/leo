#!/usr/bin/env python3

import re
import urllib.request
import argparse
import subprocess

def parseArg():
    parser = argparse.ArgumentParser(description='LeoDict for CLI')
    parser.add_argument('word', type=str, help='the word to look up')
    parser.add_argument(
        '--english', '-e', dest='lang', action='store_const',
        const='en',
        help='look up english (default)',
        default="en"
    )
    parser.add_argument(
        '--chinese', '-c', dest='lang', action='store_const',
        const='cn',
        help='look up chinese (default)'
    )
    parser.add_argument(
        '--elinks', dest='browser', action='store_const',
        const='elinks',
        help='the default browser',
        default='elinks'
    )
    parser.add_argument(
        '--w3m', dest='browser', action='store_const',
        const='w3m'
    )
    parser.add_argument(
        '--lynx', dest='browser', action='store_const',
        const='lynx'
    )
    args = parser.parse_args()
    return args


LANGSWITCH = {
        'en': 'german-english',
        'cn': 'chinesisch-deutsch'
}


def render(html, browser):
    if browser == 'elinks':
        subprocess.Popen(
            [
                'elinks',
                '-dump',
                '-no-references', '-no-numbering',
                '-dump-color-mode', '1'
            ],
            stdin=subprocess.PIPE
        ).communicate(input=html.encode())
    elif browser == 'w3m':
        subprocess.Popen(
            ['w3m', '-dump',  '-T', 'text/html'],
            stdin=subprocess.PIPE
        ).communicate(input=html.encode())
    elif browser == 'lynx':
        subprocess.Popen(
            ['lynx', '-stdin', '-dump', '-nonumbers', '-nolist'],
            stdin=subprocess.PIPE
        ).communicate(input=html.encode())





if __name__ == '__main__':
    opt = parseArg()
    req = urllib.request.Request(
        'https://dict.leo.org/{}/{}'.format(LANGSWITCH[opt.lang], opt.word),
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        html = re.sub(r'^.*?</header>', '', html, flags=re.S)
        html = re.sub(r'^.*?</header>', '', html, flags=re.S)
        html = re.sub(r'<div class="m-v-large">.*$', '', html, flags=re.S)

    render(html, opt.browser)

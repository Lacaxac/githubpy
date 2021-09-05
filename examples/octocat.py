
import argparse

from githubpy import *


def main():
    
    parser = argparse.ArgumentParser(description="Simple program to draw the 'Octocat' with ascii art")
    
    parser.add_argument('text', nargs='?', default="Hello World")
    parser.add_argument("-t", "--token", default='', help="Github Access Token")
    parser.add_argument("-v", "--verbose", action='store_true', help="display remaining rate-limit")
    
    options = parser.parse_args()
    
    ghc = GitHubClient(options.token)

    ascii_art = ghc.MetaGetOctocat(options.text).data.decode('utf-8')
    
    print(ascii_art)
    
    if options.verbose:
        print(f"rate-limit remaining={ghc.rateLimitRemaining}   reset: {ghc.rateLimitReset.strftime('%c')}")
    
    
if __name__ == '__main__':
    main()
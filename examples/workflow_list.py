
from githubpy import *


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-t", "--token")
    parser.add_argument("-o", "--owner")
    parser.add_argument("-r", "--repo")
    
    options = parser.parse_args()
    
    ghc = GitHubClient(token=options.token)

    l = ghc.ActionsListWorkflowRunsForRepo(options.owner, options.repo)
    
    return 

if __name__ == '__main__':
    main()
    
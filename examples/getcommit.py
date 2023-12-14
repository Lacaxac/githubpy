
import githubV3py

def main():
    import argparse
        
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-o", "--owner")
    parser.add_argument("-r", "--repo") 
    parser.add_argument("-t", "--token")

    options = parser.parse_args()
    

    ghc = githubV3py.GitHubClient(token=options.token)
    
    
    commits = ghc.ReposListCommits(options.owner, options.repo, sha='c0ad6e2')
    
    
    return

if __name__ == '__main__':
    main()
        
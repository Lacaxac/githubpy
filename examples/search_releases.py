
import githubV3py

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-o", "--owner")
    parser.add_argument("-r", "--repo") 
    parser.add_argument("-t", "--token")

    options = parser.parse_args()
    

    ghc = githubV3py.GitHubClient(token=options.token)     
    
    releases = ghc.ReposListReleases(options.owner, options.repo)
    
    paginator = githubV3py.GitHubClient.generate(ghc.ReposListReleases, options.owner, options.repo, per_page=10)
    
    for release in paginator:
        isinstance(release, githubV3py.Release)
        print(f"{release.name:25} isDraft: {release.draft}")
        print(release.body)
                                        
    print(f"rate-limit remaining = {ghc.rateLimitRemaining}")
    
    return

if __name__ == '__main__':
    main()
        
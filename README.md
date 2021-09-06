# Overview 

A python3 API for accessing github

# Authentication

Access tokens are generated by github at this link https://github.com/settings/tokens

# Installation

(Uploading to PyPi in the near future)

```bash
$ pip install --use-feature=in-tree-build .
```

# Usage

```python

ghc = GitHubClient(token=options.token)

ascii_art = ghc.MetaGetOctocat(options.text).data.decode('utf-8')
    
print(ascii_art)
    
print(f"rate-limit remaining={ghc.rateLimitRemaining}")

```

# Pagination

Many of github's api calls return a collection of results as a list. For example:

```python
commits = ghc.ReposListCommits("owner", "repo", per_page=30, page=1)    
```

[ResposListCommits](https://docs.github.com/rest/reference/repos#list-commits) returns a list of commits for the specified repository.  However, it will only return the first 'per_page' entries.   To get the next set of commits, increment 'page' by 1.

```python
commits = ghc.ReposListCommits("owner", "repo", per_page=30, page=1)    
```

## Automatic Pagination

Given that in many cases all of a particular set of a data is desired, a convenient class method is provided for instance methods that do pagination:

```python

commits = GitHubClient.paginate(ghc.ReposListCommits, "owner", "repo", pagination_limit=1000)

```

The first parameter is the paginating instance method and the remaining parameters are the parameters you would supply the method if calling it discretely.   The optional 'pagination_limit' parameter can be specified to put a limit on the amount of data retrieved.  If not specified GitHubClient.paginate will attempt to retrieve every record.

USE THIS METHOD WITH CAUTION.  Have some situational awareness of how much data you will be asking for.   Otherwise the [rate-limit](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) on the authentication you're using could be fully consumed.  



# Troubleshooting
## Intellisense not working in WingIDE
In order for intellisense to work under WingIDE, the 'main entry point' must import the githubpy package or import another package/module that does.   
### Corrective Action:
right click the file you wish to execute in the 'Project' tab/tool and select "Set as Main Entry Point".

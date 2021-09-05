
import sys, os
import unittest
import random

from githubpy import *

class BasicTests(unittest.TestCase):
    
    @staticmethod
    def randstring(n=10, seed="abcdefghijklmnopqrtstuvwxyzABCDEFGHIJKLMNOPQRTSTUVWXYZ"):
        "Generate a random string"
        return ''.join(random.choices(seed, k=n))
    
    def test_octocat(self):
        
        ghc = GitHubClient('')
        
        text = BasicTests.randstring()
        
        ascii_art = ghc.MetaGetOctocat(text)
        
        self.assertIsInstance(ascii_art, DataResponse)
        
        ascii_art = ascii_art.data.decode('utf-8')
        
        index = ascii_art.find(text)
        
        self.assertNotEqual(index, -1, "Could not find text that was to be rendered")
        
        
        return
    
    def test_create_delete_repo(self):
        reponame = 'foobar'
        ghc = GitHubClient(os.environ['GITHUB_TOKEN'])
        
        result = ghc.ReposDelete("GitHubPyTest", "foobar")
        self.assertTrue((isinstance(result, HttpResponse) and result.result_code == 204) or result.message == 'Not Found')
        
        
        result = ghc.ReposCreateForAuthenticatedUser(reponame, description="test repo")
        self.assertIsInstance(result, Repository)
    
        result = ghc.ReposListForAuthenticatedUser(type=None)
        found = False
        for repo in result:
            found = found or repo.name==reponame
            
        self.assertTrue(found)
            
        result = ghc.ReposDelete("GitHubPyTest", "foobar")
        
        return
        
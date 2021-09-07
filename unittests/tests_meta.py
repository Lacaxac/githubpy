
import os
import random
import unittest
from githubpy import *

class MetaTests(unittest.TestCase):
    @staticmethod
    def randstring(n=10, seed="abcdefghijklmnopqrtstuvwxyzABCDEFGHIJKLMNOPQRTSTUVWXYZ"):
        "Generate a random string"
        return ''.join(random.choices(seed, k=n))
    
    def test_metaRoot(self):
        ghc = GitHubClient()

        meta = ghc.MetaRoot()
        self.assertIsNotNone(meta)
        
        meta = ghc.MetaGet()
        self.assertIsNotNone(meta)
        
        
    def test_codes_of_conduct(self):
        ghc = GitHubClient()
        
        coc = ghc.CodesOfConductGetAllCodesOfConduct()
        self.assertIsNotNone(coc)
        
    
    def test_octocat(self):
        
        ghc = GitHubClient(token=os.environ['GITHUB_TOKEN'])
        
        text = MetaTests.randstring()
        
        ascii_art = ghc.MetaGetOctocat(text)
        
        self.assertIsInstance(ascii_art, DataResponse)
        
        ascii_art = ascii_art.data.decode('utf-8')
        
        index = ascii_art.find(text)
        
        self.assertNotEqual(index, -1, "Could not find text that was to be rendered")
        
        
        return
    
    def test_ratelimits(self):
        
        ##
        ## Test that we're getting the ratelimits correctly from the
        ## headers, using the RateLimitGet method for reference
        ##
        ## Sllight chance that we'll do queries at the 'reset' rollover
        ##
        ghc = GitHubClient(token=os.environ['GITHUB_TOKEN'])
        
        rl = ghc.RateLimitGet()
        
        self.assertEqual(rl.rate.remaining, ghc.rateLimitRemaining)
        self.assertEqual(datetime.fromtimestamp(rl.rate.reset), ghc.rateLimitReset)
        
        ghc.MetaGetOctocat("foo")
        
        self.assertEqual(rl.rate.remaining-1, ghc.rateLimitRemaining)
        
        
        return 
    
    
    
    
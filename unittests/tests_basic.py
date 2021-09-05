
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
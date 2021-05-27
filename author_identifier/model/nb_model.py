import sys
sys.path.append('D:\Projects\All Projects\Text-Author-Identification-using-Naive-Bayes')

from author_identifier.util import utils

class model:
    @staticmethod    
    def predict(text, probabilities, log_prior):
        """
        Given the dialogue (as a string), and the conditional probabilities of words (dict) in our corpus along with the 
        prior probability (float), tokenizes the dialogue and uses naive bayes to figure out which character is more likely
        to have spoken this dialogue
        """
        tokens = utils.tokenize(text)
        score = log_prior
        for tk in tokens:
            if tk in probabilities:
                score += probabilities[tk]["lambda"]
            else:
                score += probabilities["xxunk"]["lambda"]
        
        if score >= 1:
            return ("Iron Man", score)
        
        return ("Captain America", score)
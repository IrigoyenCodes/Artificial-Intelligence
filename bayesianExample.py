import re
import math
from collections import defaultdict, Counter

class BayesianEmotionClassifier:
    def __init__(self):
        # Initialize dictionaries to store our data
        self.emotion_word_counts = defaultdict(Counter)  # Word counts per emotion
        self.emotion_counts = Counter()  # Total messages per emotion
        self.total_messages = 0  # Total number of messages
        self.vocabulary = set()  # All unique words
    
    def preprocess(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        # Split into words
        return text.split()
    
    def train(self, training_data):
        """
        Train the classifier on labeled data
        training_data: list of tuples (text, emotion)
        """
        for text, emotion in training_data:
            words = self.preprocess(text)
            
            # Update counts
            self.emotion_counts[emotion] += 1
            self.total_messages += 1
            
            # Update word counts for this emotion
            for word in words:
                self.emotion_word_counts[emotion][word] += 1
                self.vocabulary.add(word)
    
    def calculate_prior(self, emotion):
        """Calculate P(Emotion)"""
        return self.emotion_counts[emotion] / self.total_messages
    
    def calculate_word_probability(self, word, emotion, alpha=1.0):
        """
        Calculate P(Word|Emotion) with Laplace smoothing
        alpha: smoothing parameter (default=1.0 for Laplace smoothing)
        """
        # Number of times this word appears in this emotion
        word_count = self.emotion_word_counts[emotion][word]
        
        # Total words in this emotion
        total_words = sum(self.emotion_word_counts[emotion].values())
        
        # Calculate probability with Laplace smoothing
        return (word_count + alpha) / (total_words + alpha * len(self.vocabulary))
    
    def classify(self, text):
        """
        Classify a message using Bayes' theorem
        Returns the most likely emotion and the probabilities for all emotions
        """
        words = self.preprocess(text)
        probabilities = {}
        
        # Calculate posterior probability for each emotion
        for emotion in self.emotion_counts:
            # Start with log of prior probability
            probabilities[emotion] = math.log(self.calculate_prior(emotion))
            
            # Add log probabilities of each word given this emotion
            for word in words:
                if word in self.vocabulary:  # Only consider words we've seen in training
                    probabilities[emotion] += math.log(self.calculate_word_probability(word, emotion))
        
        # Find emotion with highest probability
        most_likely_emotion = max(probabilities, key=probabilities.get)
        
        # Convert log probabilities back to regular probabilities and normalize
        log_probs = list(probabilities.values())
        max_log_prob = max(log_probs)
        exp_probs = [math.exp(p - max_log_prob) for p in log_probs]
        sum_probs = sum(exp_probs)
        normalized_probs = {emotion: exp_probs[i]/sum_probs 
                           for i, emotion in enumerate(probabilities.keys())}
        
        return most_likely_emotion, normalized_probs


# Example usage with a small sample dataset
def create_sample_dataset():
    """Create a small sample dataset for demonstration"""
    return [
        ("I am feeling so happy today!", "happy"),
        ("What a wonderful day, I'm so excited", "happy"),
        ("I'm thrilled about my promotion", "happy"),
        ("This is the best thing ever", "happy"),
        ("I'm so sad about what happened", "sad"),
        ("I feel terrible, everything went wrong", "sad"),
        ("I miss my old friends so much", "sad"),
        ("Nothing is going right for me", "sad"),
        ("Why is this happening to me?", "angry"),
        ("I can't believe they did this!", "angry"),
        ("This is so frustrating and annoying", "angry"),
        ("I hate when people lie to me", "angry"),
        ("I'm worried about the upcoming exam", "anxious"),
        ("What if everything goes wrong tomorrow?", "anxious"),
        ("I'm feeling really nervous about the presentation", "anxious"),
        ("I can't stop thinking about all the things that could go wrong", "anxious")
    ]

def main():
    # Create and train the classifier
    classifier = BayesianEmotionClassifier()
    training_data = create_sample_dataset()
    classifier.train(training_data)
    
    # Allow user to input a message and get the emotion classification
    while True:
        user_input = input("\nEnter a message (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        emotion, probabilities = classifier.classify(user_input)
        
        print(f"\nDetected emotion: {emotion.upper()}")
        print("\nProbabilities for all emotions:")
        for e, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
            print(f"{e}: {prob:.2%}")

if __name__ == "__main__":
    main()
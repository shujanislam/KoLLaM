from .general_classifier import PredictImage

def test_prediction(path):
    prob = PredictImage(path)
    print(f"Kolam Probability: {prob:.4f}")
    print(prob)
    return { prob }


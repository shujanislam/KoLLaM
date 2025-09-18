import general_classifier

def test_prediction(path):
    prob = general_classifier.PredictImage(path)
    print(f"Kolam Probability: {prob:.4f}")
    print(prob)
    return { prob }

test_prediction("./dataset/general_classifier/valid_kolam_s03_i053_lavender.png")

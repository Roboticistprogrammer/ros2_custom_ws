# Import necessary libraries
import torch
import matplotlib.pyplot as plt
from PIL import Image
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation

def main():
    # Load models
    processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
    model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

    # Load and show image
    img_path = "/home/user/ros2_ws/src/vision_language_models/images/dog.jpeg"
    image = Image.open(img_path)
    image.show()

    # User input for object segmentation
    texts_input = input("Make a list of the objects to be segmented separated by commas. Example: Item1,Item2,...,ItemN >>>>")
    texts = [text.strip() for text in texts_input.split(",")]

    # Process the inputs
    inputs = processor(text=texts, images=[image] * len(texts), padding=True, return_tensors="pt")

    # Get outputs
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    print(logits.shape)
    logits = logits.unsqueeze(1)
    print(logits.shape)

    # Plot results
    _, ax = plt.subplots(1, len(texts) + 1, figsize=(3*(len(texts) + 1), 12))
    [a.axis('off') for a in ax.flatten()]
    ax[0].imshow(image)
    [ax[i+1].imshow(torch.sigmoid(logits[i][0])) for i in range(len(texts))]
    [ax[i+1].text(0, -15, text) for i, text in enumerate(texts)]
    
    plt.show()

if __name__ == "__main__":
    main()


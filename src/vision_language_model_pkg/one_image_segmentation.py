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
    texts = ["dog"]

    # Process the inputs
    inputs = processor(text=texts, images=image, padding=True, return_tensors="pt")

    # Get outputs
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits

    # Process the logits
    image = torch.sigmoid(logits).numpy()

    # Plot results
    print("LENGTH="+str(len(texts)))
    print(image.shape)
    plt.imshow(image)

    plt.axis('off')  # Hide axis
    plt.show()

if __name__ == "__main__":
    main()

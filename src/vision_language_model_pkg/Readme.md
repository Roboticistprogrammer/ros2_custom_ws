Source https://www.youtube.com/watch?v=mjgoXucDfeA&list=WL&index=1&t=816s

Some examples of these models are:
CLIP, OPENAI CLIP
FLAVA
GIT
BridgeTower
GroupViT
BLIP
OWL-ViT
CLIPSeg
X-CLIP
VisualBERT
ViLT
LiT (an instance of the VisionTextDualEncoder)
TrOCR (an instance of the VisionEncoderDecoderModel)
VisionTextDualEncoder
VisionEncoderDecoderModel
Models like CLIP, FLAVA, BridgeTower, BLIP, LiT, and VisionEncoderDecoder offer joint image-text embedding for tasks like zero-shot image classification. FLAVA is versatile, supporting unimodal (vision or language) and multi-modal tasks due to its mixed pretraining objectives.


--
Function main():

Model Loading:

processor and model are initialized with pretrained weights from the given path "CIDAS/clipseg-rd64-refined".
Image Handling:

An image of a dog is loaded from the specified path and then displayed to the user using image.show().
User Input:

The user is prompted to list objects they want to segment from the image. They should separate each item with a comma.
Data Processing:

The user's input is processed using the processor to format it appropriately for the model.
The image is duplicated and processed for each object the user wants to segment.
Model Inference:

Predictions (or segmentations) are made for each object in the user's list using the model. The result is stored in logits.
logits are then processed further to prepare them for visualization.
Visualization:

The original image and segmentations of the listed objects are plotted side by side.
Each segmented image is labeled with the corresponding object name the user provided.
The plot is displayed to the user using plt.show().
Script Execution:

The if __name__ == "__main__": line ensures that the main() function is executed only when this script is run directly (not when imported as a module).

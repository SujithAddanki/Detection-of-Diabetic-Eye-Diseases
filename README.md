👁️ EyeGuard: AI-Powered Eye Disease Detection
Welcome to EyeGuard, an innovative deep learning project designed to detect eye diseases such as cataracts, diabetic retinopathy (DR), glaucoma, and normal conditions using retinal images. Leveraging the power of the EfficientNet-B3 model, EyeGuard aims to assist medical professionals in early diagnosis, potentially saving vision and improving lives.

🌟 Project Overview
EyeGuard is a convolutional neural network (CNN) based solution built with PyTorch and the EfficientNet-B3 architecture. It classifies retinal images into four categories: Cataract, Diabetic Retinopathy (DR), Glaucoma, and Normal. The model is trained on a dataset of retinal images, achieving high accuracy through transfer learning and fine-tuning.
This project is ideal for researchers, developers, and healthcare enthusiasts interested in applying AI to medical imaging. Whether you're exploring computer vision or aiming to contribute to healthcare innovation, EyeGuard is a great starting point!

🚀 Features

Advanced Model: Utilizes EfficientNet-B3, pre-trained on ImageNet, fine-tuned for eye disease classification.
High Accuracy: Achieves robust performance with a focus on precision for medical applications.
Data Preprocessing: Includes image resizing, normalization, and augmentation for optimal model training.
Comprehensive Evaluation: Provides classification reports, confusion matrices, and visualizations for performance analysis.
User-Friendly Prediction: Easily predict eye conditions from new images using a single function.
Modular Code: Well-structured Jupyter Notebook (final_model.ipynb) for easy experimentation and extension.


🛠️ Installation
To get started with EyeGuard, follow these steps to set up the environment:
Prerequisites

Python 3.8+
CUDA-enabled GPU (optional, for faster training)
Git



STEPS


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install torch torchvision timm scikit-learn matplotlib seaborn h5py pillow


Download the Dataset:

Place your dataset in the dataset/ folder with subdirectories for each class (cataract, DR, glaucoma, normal).
Update the dataset path in final_model.ipynb (Cell 3) to point to your dataset location.


(Optional) Download Pre-trained Model:

Download the pre-trained model weights (eye_disease_model.pth) from the Releases section and place it in the project root.




📊 Dataset
The dataset used for training consists of retinal images categorized into four classes:

Cataract: Cloudy areas in the lens of the eye.
Diabetic Retinopathy (DR): Damage to retinal blood vessels due to diabetes.
Glaucoma: Optic nerve damage, often linked to increased eye pressure.
Normal: Healthy retinal images.

Note: Due to privacy and size constraints, the dataset is not included in this repository. You can use publicly available datasets like Kaggle's Eye Disease Dataset or prepare your own. Ensure the dataset is organized in the following structure:
dataset/
├── cataract/
├── DR/
├── glaucoma/
├── normal/


🧠 Model Details

Architecture: EfficientNet-B3
Input Size: 300x300 pixels
Classes: 4 (Cataract, DR, Glaucoma, Normal)
Training Setup:
Batch Size: 32
Epochs: 30
Learning Rate: 0.0001
Optimizer: Adam
Loss Function: Cross-Entropy Loss


Preprocessing: Images are resized, normalized (mean=0.5, std=0.5), and converted to tensors.

The model is fine-tuned from ImageNet weights, with the final fully connected layer modified to output predictions for the four classes.

▶️ Usage

Train the Model:

Open final_model.ipynb in Jupyter Notebook or JupyterLab.
Update the dataset path in Cell 3.
Run all cells to train the model. The trained model will be saved as eye_disease_model.pth.


Make Predictions:

Use the predict_image function in Cell 5 to classify a new retinal image:image_path = "path/to/your/image.jpg"
predict_image(image_path, inference_model, transform, classes)


The function will display the input image and print the predicted class.


Evaluate Performance:

Run the evaluation cells to generate classification reports and confusion matrices (see Cell 4 for model loading and inference setup).




📈 Performance
The model achieves high accuracy on the test set, with detailed metrics provided in the notebook:

Classification Report: Precision, recall, and F1-score for each class.
Confusion Matrix: Visualized using Seaborn for easy interpretation.

Example prediction output:
Predicted Class: Glaucoma

For detailed performance metrics, refer to the notebook's evaluation section.

🤝 Contributing
We welcome contributions to improve EyeGuard! Here's how you can get involved:

Fork the Repository: Click the "Fork" button on GitHub.
Create a Branch:git checkout -b feature/your-feature-name




📜 License
This project is licensed under the MIT License. See the LICENSE file for details.





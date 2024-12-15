# AIR Canvas - Virtual Paint Application

A real-time object tracking and drawing application built using OpenCV. This project allows users to draw on a virtual canvas by tracking the movement of an object of a specific color (which can be calibrated by the user). The application provides color switching options and a clear button for the canvas.

## Deployed Link
You can try the deployed version of the app here:  
[**AIR Canvas - Deployed App**](https://aircanvas-hkkzcuqodx4hmobscv44j6.streamlit.app/)

## GitHub Link
For the project source code and more details, visit:  
[**AIR Canvas - GitHub Repository**](https://github.com/Tanendra77/AIR_Canvas)

## Features
- Real-time object tracking using OpenCV.
- Dynamic calibration of marker color using HSV trackbars.
- Color switching options: Blue, Green, Red, and Yellow.
- Clear the canvas with a button click.
- Interactive and user-friendly interface.
- No machine learning used – the application relies solely on C.V for object tracking.
- Doesn't require a powerful system – works efficiently on most standard computers.

## Requirements

Before running the application locally, ensure you have the following:

- Python 3.6 or higher

## Installation & Setup

To run the application locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/Tanendra77/AIR_Canvas.git

# Navigate to the project folder
cd AIR_Canvas

# Create a virtual environment
python -m venv venv

# Activate the virtual environment

# For Windows:
./venv/Scripts/activate

# For MacOS/Linux:
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Run the application using Streamlit
streamlit run main.py

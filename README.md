# Django PDF to Audio Converter

This Django project provides a web application to convert PDF files to audio format. Users can upload PDF files, select desired settings, and generate corresponding audio files. This README provides a guide on how to set up and use the application.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Sebifrancis1935/pdf-to-audio-converter-website

Navigate into the project directory:

cd django-pdf-to-audio

Install the required dependencies using pip:

pip install -r requirements.txt

Usage

Start the Django development server:

python manage.py runserver

Open a web browser and navigate to http://localhost:8000/ to access the application.

Upload the PDF file you want to convert to audio.

Select desired settings such as language, voice, and output format.

Click on the "Convert" button to initiate the conversion process.

Once the conversion is complete, you will be able to download the generated audio file.

Configuration
The application comes with default settings for language, voice, and output format. However, you can customize these settings by modifying the appropriate configuration files or through the web interface.

Development
If you wish to contribute to the development of this project, you can follow these steps to set up a development environment:

Fork the repository on GitHub.

Clone your forked repository to your local machine.

Create a new branch for your changes:

git checkout -b feature/your-feature-name

Make your changes and commit them to your branch:

git commit -am "Add your commit message here"

Push your changes to your forked repository:

git push origin feature/your-feature-name

Open a pull request on GitHub, comparing your branch with the main branch of the original repository.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
This project utilizes Django framework.
Audio conversion is facilitated by libraries such as PyPDF2 and Google Text-to-Speech API.

This README provides an overview of how to install, use, and contribute to the Django PDF to Audio Converter project. Make sure to replace placeholders like `your_username` with appropriate values specific to your repository.

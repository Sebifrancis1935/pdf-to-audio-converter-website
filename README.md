# PDF to Audio Converter

This Django project is a web application that allows users to convert PDF files into audio format. It's a convenient tool for individuals who prefer listening to documents instead of reading them. With this application, users can upload PDF files, select their preferred settings, and generate corresponding audio files.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Installation

1. Clone this repository to your local machine:

git clone https://github.com/your_username/pdf-to-audio.git


2. Navigate into the project directory:

cd pdf-to-audio


3. Create a virtual environment named `env`:

python -m venv env


4. Activate the virtual environment:

On Windows:


On macOS and Linux:

source env/bin/activate


5. Install the required dependencies using pip:

pip install -r requirements.txt


## Usage

1. Start the Django development server:

python manage.py runserver


2. Open a web browser and navigate to `http://localhost:8000/` to access the application.

3. Upload the PDF file you want to convert to audio.

4. Select desired settings such as language, voice, and output format.

5. Click on the "Convert" button to initiate the conversion process.

6. Once the conversion is complete, you will be able to download the generated audio file.

## Configuration

The application comes with default settings for language, voice, and output format. However, you can customize these settings by modifying the appropriate configuration files or through the web interface.

## Development

If you wish to contribute to the development of this project, you can follow these steps to set up a development environment:

1. Fork the repository on GitHub.

2. Clone your forked repository to your local machine.

3. Create a new branch for your changes:

git checkout -b feature/your-feature-name


4. Make your changes and commit them to your branch:

git commit -am "Add your commit message here"


5. Push your changes to your forked repository:

git push origin feature/your-feature-name


6. Open a pull request on GitHub, comparing your branch with the `main` branch of the original repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project utilizes the [Django](https://www.djangoproject.com/) framework.
- Audio conversion is facilitated by libraries such as [PyPDF2](https://pythonhosted.org/PyPDF2/) and [Google Text-to-Speech API](https://cloud.google.com/text-to-speech).

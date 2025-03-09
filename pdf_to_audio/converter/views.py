from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect
from .models import UploadedPDF
from PyPDF2 import PdfReader
from gtts import gTTS
import os


import os
from django.shortcuts import render, redirect
from django.conf import settings
from speech_recognition import Recognizer, AudioFile
from .models import UploadedPDF
from .forms import UploadAudioForm

def convert_audio_to_text(request):
    if request.method == 'POST':
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded audio file
            uploaded_audio = form.save()

            # Define the audio file path
            audio_file_path = uploaded_audio.audio_file.path

            # Initialize SpeechRecognition
            recognizer = Recognizer()
            try:
                # Process the audio file using SpeechRecognition
                with AudioFile(audio_file_path) as source:
                    audio_data = recognizer.record(source)  # Record the audio data
                    text = recognizer.recognize_google(audio_data)  # Convert to text

                # Define the path to save the text file
                text_file_name = os.path.splitext(uploaded_audio.audio_file.name)[0] + '.txt'
                text_file_path = os.path.join(settings.MEDIA_ROOT, 'texts', text_file_name)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(text_file_path), exist_ok=True)

                # Save the recognized text to a text file
                with open(text_file_path, 'w') as text_file:
                    text_file.write(text)

                # Update the model to store the text file's relative path
                uploaded_audio.text_file = os.path.join('texts', text_file_name)
                uploaded_audio.save()

                # Render a page to download or display the text file
                return render(request, 'download_text.html', {
                    'text_file_url': os.path.join(settings.MEDIA_URL, 'texts', text_file_name),
                    'recognized_text': text
                })

            except Exception as e:
                # Handle errors during audio processing
                return render(request, 'error.html', {'error': f"Error processing audio: {str(e)}"})
        else:
            return render(request, 'error.html', {'error': 'Invalid form submission'})
    else:
        form = UploadAudioForm()

    return render(request, 'upload_audio.html', {'form': form})



def index(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'index_about.html')


def contact_us(request):
    return render(request, 'index_contact.html')


def contact(request):
    return render(request, 'contact.html')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,  'user_registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return render(request, 'home.html')

                # return redirect('upload_pdf')
    else:
        form = AuthenticationForm()
    return render(request,  'user_login.html', {'form': form})


import pyttsx3
import pdfplumber

@login_required
def convert_pdf_to_audio(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        language = request.POST.get('language')
        uploaded_pdf = UploadedPDF.objects.create(file=file, language=language, user=request.user)

        # Use pdfplumber for faster text extraction
        with pdfplumber.open(uploaded_pdf.file.path) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())

        # Use pyttsx3 for TTS
        engine = pyttsx3.init()
        audio_directory = 'audios'
        os.makedirs(audio_directory, exist_ok=True)
        audio_file_path = os.path.join(
            audio_directory, uploaded_pdf.file.name.split('/')[-1].replace('.pdf', '.mp3'))
        engine.save_to_file(text, audio_file_path)
        engine.runAndWait()

        uploaded_pdf.audio_file = audio_file_path
        uploaded_pdf.save()
        return redirect('view_files')

    return render(request, 'upload_pdf.html')
@login_required
def convert_audio_to_text(request):
    if request.method == 'POST':
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded audio file and associate it with the current user
            uploaded_audio = form.save(commit=False)
            uploaded_audio.user = request.user  # Associate with the current user
            uploaded_audio.save()

            # Define the audio file path
            audio_file_path = uploaded_audio.audio_file.path

            # Initialize SpeechRecognition
            recognizer = Recognizer()
            try:
                # Process the audio file using SpeechRecognition
                with AudioFile(audio_file_path) as source:
                    audio_data = recognizer.record(source)  # Record the audio data
                    text = recognizer.recognize_google(audio_data)  # Convert to text

                # Define the path to save the text file
                text_file_name = os.path.splitext(uploaded_audio.audio_file.name)[0] + '.txt'
                text_file_path = os.path.join(settings.MEDIA_ROOT, 'texts', text_file_name)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(text_file_path), exist_ok=True)

                # Save the recognized text to a text file
                with open(text_file_path, 'w') as text_file:
                    text_file.write(text)

                # Update the model to store the text file's relative path
                uploaded_audio.text_file = os.path.join('texts', text_file_name)
                uploaded_audio.save()

                # Render a page to download or display the text file
                return render(request, 'download_text.html', {
                    'text_file_url': os.path.join(settings.MEDIA_URL, 'texts', text_file_name),
                    'recognized_text': text
                })

            except Exception as e:
                # Handle errors during audio processing
                return render(request, 'error.html', {'error': f"Error processing audio: {str(e)}"})
        else:
            return render(request, 'error.html', {'error': 'Invalid form submission'})
    else:
        form = UploadAudioForm()

    return render(request, 'upload_audio.html', {'form': form})

def pdf_to_audio(request):
    if request.method == 'POST':
        pdf_id = request.POST.get('pdf_id')
        language = request.POST.get('language')
        uploaded_pdf = get_object_or_404(UploadedPDF, pk=pdf_id)

        with open(uploaded_pdf.file.path, 'rb') as pdf_file:
            pdf = PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf.pages)):
                text += pdf.pages[page_num].extract_text()

        tts = gTTS(text, lang=language)
        audio_directory = 'audios'
        os.makedirs(audio_directory, exist_ok=True)
        audio_file_path = os.path.join(
            audio_directory, uploaded_pdf.file.name.split('/')[-1].replace('.pdf', f'_{language}.mp3'))
        tts.save(audio_file_path)

        uploaded_pdf.audio_file = audio_file_path
        uploaded_pdf.save()
        return redirect('view_files')

    return render(request,  'upload_pdf.html')


@login_required
def view_files(request):
    # Filter UploadedPDF objects by the currently logged-in user
    uploaded_pdfs = UploadedPDF.objects.filter(user=request.user)

    if request.method == 'POST' and 'delete_file' in request.POST:
        pdf_id = request.POST.get('pdf_id')
        audio_id = request.POST.get('audio_id')
        try:
            pdf_obj = UploadedPDF.objects.get(pk=pdf_id, user=request.user)  # Ensure the user owns the file
            if audio_id:
                audio_obj = UploadedPDF.objects.get(pk=audio_id, user=request.user)  # Ensure the user owns the file
                if audio_obj.audio_file:
                    os.remove(audio_obj.audio_file.path)
                audio_obj.delete()
            if pdf_obj.file:
                os.remove(pdf_obj.file.path)
            pdf_obj.delete()
            return HttpResponseRedirect(reverse('view_files'))
        except Exception as e:
            return HttpResponseRedirect(reverse('view_files'))

    return render(request, 'view_files.html', {'uploaded_pdfs': uploaded_pdfs})

def download_audio(request, pk):
    uploaded_pdf = UploadedPDF.objects.get(pk=pk)
    audio_file_path = uploaded_pdf.audio_file.path
    return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')


def user_logout(request):
    auth_logout(request)
    return redirect('login')


def delete_file(request):
    if request.method == 'POST':
        pdf_id = request.POST.get('pdf_id')
        audio_id = request.POST.get('audio_id')
        try:
            pdf_obj = UploadedPDF.objects.get(pk=pdf_id)

            # Check if the PDF object has an associated audio file
            if pdf_obj.audio_file:
                # Delete the associated audio file
                if os.path.exists(pdf_obj.audio_file.path):
                    os.remove(pdf_obj.audio_file.path)
                pdf_obj.audio_file.delete()

            # Delete the PDF file itself
            if pdf_obj.file:
                if os.path.exists(pdf_obj.file.path):
                    os.remove(pdf_obj.file.path)
                pdf_obj.file.delete()

            # Finally, delete the PDF object from the database
            pdf_obj.delete()

            return HttpResponseRedirect(reverse('view_files'))
        except Exception as e:
            # Handle exceptions
            return HttpResponseRedirect(reverse('view_files'))
    else:
        # Redirect to view_files in case of GET request
        return HttpResponseRedirect(reverse('view_files'))
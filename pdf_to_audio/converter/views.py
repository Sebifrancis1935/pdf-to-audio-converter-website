from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
import os
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from .models import UploadedPDF
from PyPDF2 import PdfReader
from gtts import gTTS
from django.http import FileResponse


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'converter/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('upload_pdf')
    else:
        form = AuthenticationForm()
    return render(request, 'converter/login.html', {'form': form})


def convert_pdf_to_audio(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        language = request.POST.get('language')
        uploaded_pdf = UploadedPDF.objects.create(file=file, language=language)
        pdf = PdfReader(uploaded_pdf.file)
        text = ''
        for page_num in range(len(pdf.pages)):
            text += pdf.pages[page_num].extract_text()
        tts = gTTS(text, lang=uploaded_pdf.language)
        audio_directory = 'audios'
        os.makedirs(audio_directory, exist_ok=True)
        audio_file_path = os.path.join(
            audio_directory, uploaded_pdf.file.name.split('/')[-1].replace('.pdf', '.mp3'))
        tts.save(audio_file_path)
        uploaded_pdf.audio_file = audio_file_path
        uploaded_pdf.save()
        return redirect('view_files')
    return render(request, 'converter/upload_pdf.html')


def view_files(request):
    pdf_files = os.listdir('pdfs')
    audio_files = os.listdir('audios')

    # Combine PDF and audio files into a single list of tuples
    files = zip(pdf_files, audio_files)

    return render(request, 'converter/view_files.html', {'files': files})

    pdf_files = os.listdir('pdfs')
    audio_files = os.listdir('audios')
    return render(request, 'converter/view_files.html', {'pdf_files': pdf_files, 'audio_files': audio_files})


def download_audio(request, pk):
    uploaded_pdf = UploadedPDF.objects.get(pk=pk)
    audio_file_path = uploaded_pdf.audio_file.path
    return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')


def user_logout(request):
    auth_logout(request)
    return redirect('login')

from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import render, redirect
from .models import UploadedPDF
from PyPDF2 import PdfReader
from gtts import gTTS
import os


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

        # Ensure file handle is properly closed after use
        with open(uploaded_pdf.file.path, 'rb') as pdf_file:
            pdf = PdfReader(pdf_file)
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
    uploaded_pdfs = UploadedPDF.objects.all()

    if request.method == 'POST' and 'delete_file' in request.POST:
        pdf_id = request.POST.get('pdf_id')
        audio_id = request.POST.get('audio_id')
        try:
            pdf_obj = UploadedPDF.objects.get(pk=pdf_id)
            if audio_id:
                audio_obj = UploadedPDF.objects.get(pk=audio_id)
                if audio_obj.audio_file:
                    os.remove(audio_obj.audio_file.path)
                audio_obj.delete()
            if pdf_obj.file:
                os.remove(pdf_obj.file.path)
            pdf_obj.delete()
            return HttpResponseRedirect(reverse('view_files'))
        except Exception as e:
            return HttpResponseRedirect(reverse('view_files'))

    return render(request, 'converter/view_files.html', {'uploaded_pdfs': uploaded_pdfs})


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

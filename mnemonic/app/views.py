from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from .forms import FileUploadForm,AudioUploadForm
from .models import FileUpload,AudioUpload
import PyPDF2
import openai
# Create your views here.
sample_output = ""
text_summary = ""
file_name = ""
audio_output = ""

@csrf_exempt
def home(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        table = models.login(email=email, password=password)
        table.save()
        return redirect("choice")
    return render(request, 'home.html')

def upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            form.save()
            global sample_output
            global text_summary
            global file_name
            file_name = "E:\\megan\\project\\MNEMONIC\\mnemonic\\app\\file\\" + uploaded_file.name
            sample_output = Process_PDF(file_name)
            text_summary = extractive_summarization(str(sample_output))
            return redirect("/readfile")
    else:
        form = FileUploadForm()
    return render(request, "upload.html", {'form': form})

def file_list(request):
    files = FileUpload.objects.all()
    return render(request, 'file_list.html', {'files': files})

def read_file(request):
    return render(request, "sample_output.html", {'text_summary': text_summary})

def Process_PDF(filename):
    try:
        with open(filename, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                extracted_text += page_text
            pdf_file.close()
            return extracted_text
    except FileNotFoundError:
        print("File not found")

def choice(request):
    return render(request, 'choice.html')

def audio(request):
    if request.method == "POST":
        audio_form = AudioUploadForm(request.POST, request.FILES)
        if audio_form.is_valid():
            uploaded_file = request.FILES['file']
            audio_form.save()
            file_name_audio = "E:\\megan\\project\\MNEMONIC\\mnemonic\\app\\audio\\" + uploaded_file.name
            import deepspeech
            import wave
            model_path = 'path_to_pretrained_model/output_graph.pb'
            model = deepspeech.Model(model_path)
            with wave.open(file_name_audio, 'rb') as audio:
                audio_data = audio.readframes(audio.getnframes())
                sample_rate = audio.getframerate()
            text = model.stt(audio_data, sample_rate)
            global audio_output
            audio_output = text
            redirect("home")
    else:
        audio_form = FileUploadForm()
    return render(request, 'audio.html', {'form':audio_form})

def audio_text(request):
    return render(request,"audio_text.html", {'audio_output':audio_output})

import nltk
from transformers import BartForConditionalGeneration, BartTokenizer

nltk.download("stopwords")
def extractive_summarization(text):
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True, padding=True)
    # Generate the summary
    summary_ids = model.generate(inputs["input_ids"], max_length=1024, min_length=256, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = ""
    for summary_id in summary_ids:
        summary += tokenizer.decode(summary_id, skip_special_tokens=True)
    return summary

from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email
            send_mail(
                subject,
                f"From: {name}\nEmail: {email}\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            # Show success message
            messages.success(request, 'Your message has been sent successfully.')
            
            # Redirect to the same page
            return redirect('index')
    else:
        form = ContactForm()
    return render(request,'index.html',{'form': form})


def download_pdf(request):
    # Path to your .pdf file
    pdf_file_path = os.path.join(settings.STATICFILES_DIRS[1], 'online resume.pdf')

    # Open the .pdf file and read its content
    with open(pdf_file_path, 'rb') as file:
        pdf_data = file.read()

    # Create the HttpResponse object with the appropriate MIME type
    response = HttpResponse(pdf_data, content_type='application/pdf')
    
    # Set the HTTP headers for file download
    response['Content-Disposition'] = 'attachment; filename="online resume.pdf"'
    
    return response
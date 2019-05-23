from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm

def Contact(request):
    contactform = ContactForm()
    if request.method == 'POST':
        # instantiate the form 
        contactform = ContactForm(request.POST)
        if contactform.is_valid():
            #Form fields passed validation

            cd = contactform.cleaned_data
            print(cd)
            # ... send email
            name = cd['name']
            subject = cd['subject']
            from_email = cd['email']
            message = cd['message']
            try:
                send_mail(subject, message, from_email, ['mail@achiengcindy.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('success')

    return render(request, 'contact.html', {'contactform': contactform})



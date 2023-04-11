import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TicketModel
import random


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

# Authentication Imports start 
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user
from django.contrib.auth.models import Group
# Authentication Imports end 


# Create your views here.
# login User 
@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    return render(request, "Authentication/login.html")


# logout user 
def LogoutUser(request):
    logout(request)
    return redirect('login')

def adminOnly(request):
    return render(request,'client/admin_only.html')



@allowed_user(allowed_roles=['admin'])
def IndexView(request):
    list_tickets = TicketModel.objects.all().order_by('arrived', '-date_created')
    arrived_count = TicketModel.objects.filter(arrived ='Yes').count()
    pending = TicketModel.objects.filter(arrived ='No').count()

    context = {
        "list_tickets" : list_tickets,
        "arrived_count" : arrived_count,
        "pending" : pending

    }

    return render(request,'client/index.html',context)


@allowed_user(allowed_roles=['admin'])
def TicketForm(request):
    if request.method == 'POST' and 'submit_ticket' in request.POST:
        create_ticket = TicketModel()
        create_ticket.ticket_number = random.randrange(0, 100000000)
        create_ticket.first_name = request.POST.get('first_name')
        create_ticket.last_name = request.POST.get('Last_name')
        create_ticket.phone  = request.POST.get('phone')
        create_ticket.email = request.POST.get('email')

        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        data = 'http://192.168.1.119:8000/ticket/' + str(create_ticket.ticket_number)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        # Save QR code image to model
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_image = ContentFile(buffer.getvalue())
        create_ticket.qr_code.save(f'{create_ticket.ticket_number}.png', qr_image)

        create_ticket.save()
        messages.success(request,'New Ticket Successfully Created') 
        return redirect('ticket', create_ticket.ticket_number )

    return render(request,'client/create_ticket.html', {})


@allowed_user(allowed_roles=['admin'])
def TicketDetailsModel(request,id):
    ticket = TicketModel.objects.get(ticket_number = id)

    ticketNumber = id 
    request.session['ticketnumber'] = ticketNumber

    if request.method == 'POST' and 'confirm_ticket' in request.POST:
        confirm_arrival = TicketModel.objects.get(ticket_number = id)
        confirm_arrival.arrived = 'Yes'
        confirm_arrival.save()
        messages.success(request,'Successfully Updated') 
        return redirect('ticket', id )
    
    if request.method == 'POST' and 'unconfirm' in request.POST:
        un_confirm_arrival = TicketModel.objects.get(ticket_number = id)
        un_confirm_arrival.arrived = 'No'
        un_confirm_arrival.save()
        messages.success(request,'Successfully Updated') 
        return redirect('ticket', id )

    context = {
        "ticket" : ticket
    }
    return render(request,'client/ticket.html',context)


def PDFTemplate(request,id):
    pdf_data = TicketModel.objects.get(ticket_number = id)
    qr_code_name = os.path.basename(pdf_data.qr_code.name)

    context = {
        "pdf_data" : pdf_data,
        "qr_code_name" : qr_code_name
    }
    return render(request,'client/pdf_template.html',context)


def generate_pdf(request):
    #get ticket from session storage
    ticketnumber = request.session.get('ticketnumber')
    pdf_data = TicketModel.objects.get(ticket_number = ticketnumber)
    qr_code_name = os.path.basename(pdf_data.qr_code.name)

    # Generate the HTML page
    template = get_template('client/pdf_template.html')
    html = template.render({'pdf_data': pdf_data, 'qr_code_name': qr_code_name}, request=request)

    # Create a BytesIO buffer to receive the PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    pisa.CreatePDF(html, dest=buffer)

    # Use the content of the BytesIO buffer to create a response.
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')

    # Set the filename of the PDF attachment.
    response['Content-Disposition'] = f'attachment; filename="{ticketnumber}.pdf"'

    return response

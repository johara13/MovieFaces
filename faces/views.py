# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Document
from faces.forms import DocumentForm
from django.utils import timezone
from faces.utils import main, grab_frame
import PIL

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('results', args=(newdoc.id,)))
            #return render(request, 'index.html', {'ifile':newdoc.docfile.url})
            #return HttpResponseRedirect(reverse('results',args=(newdoc.pk,)))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'index.html',
        {'documents': documents, 'form': form,}
    )


class IndexView(generic.ListView):
    template_name = 'faces/index.html'
    context_object_name = 'latest_upload_list'
    #videofile = "C:/Users/wildcat/facesproject/faces/static/faces/images/jurassicparkf.mp4"
    #grab_frame(videofile, 100)

    def get_queryset(self):
        return None

def results(request, document_id):
    doc = get_object_or_404(Document, pk=document_id)
    ifile = doc.docfile.url

    #analyzes pictures just created and makes sure they won't be analyzed for a second time
    if not doc.analyzed:
        #splits video into picture ~2-4 seconds
        grab_frame(ifile)
        main(doc, 4)
        doc.analyzed = True
        doc.save()

    #for testing purposes
    #videofile = "C:/Users/wildcat/facesproject/faces/static/faces/images/jurassicparkf.mp4"
    #grab_frame(videofile)
    #main(videofile, 4)

    #grabs list of all Documents
    documents = Document.objects.all()
    #unbound form
    form = DocumentForm()
    return render(request, 'index.html', {'documents':documents, 'form':form, 'ifile':doc})




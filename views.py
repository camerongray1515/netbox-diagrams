from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from urllib import unquote
from diagrams.models import Diagram

def index(request):
    diagrams = Diagram.objects.all()
    return render(request, "diagrams/list.html", {
        "diagrams": diagrams
    })

def editor(request, diagram_id=None):
    diagram_xml = None
    diagram_filename = None
    if diagram_id:
        try:
            diagram = Diagram.objects.get(id=diagram_id)
            diagram_xml = diagram.diagram
            diagram_filename = diagram.name
        except (ObjectDoesNotExist, ValueError) as ex:
            raise Http404

    return render(request, "diagrams/editor.html", {
        "diagram_xml": diagram_xml,
        "diagram_filename": diagram_filename,
        "diagram_id": diagram_id
    })

def export(request, diagram_id):
    try:
        diagram = Diagram.objects.get(id=diagram_id)
    except (ObjectDoesNotExist, ValueError) as ex:
        raise Http404

    response = HttpResponse(diagram.diagram, content_type='application/xml')
    response["Content-Disposition"] = "attachment; filename=\"{}.xml\"".format(diagram.name.replace("\"", "\\\""))
    return response

def delete(request, diagram_id):
    try:
        diagram = Diagram.objects.get(id=diagram_id)
    except (ObjectDoesNotExist, ValueError) as ex:
        raise Http404

    if request.method == "POST":
        diagram.delete()
        return redirect(reverse("diagrams:index"))
    else:
        return render(request, "utilities/obj_delete.html", {
            "obj_type": "diagram",
            "obj": diagram.name,
            "cancel_url": reverse("diagrams:index")
        })

@csrf_exempt
def update(request):
    if request.method == "POST":
        filename = unquote(request.POST.get("filename"))
        xml = unquote(request.POST.get("xml"))
        diagram_id = unquote(request.POST.get("diagram_id"))

        try:
            diagram = Diagram.objects.get(id=diagram_id)
        except ObjectDoesNotExist as ex:
            return JsonResponse({"success": False,
                "message": "Diagram does not exist!"})

        if Diagram.objects.filter(name=filename).exclude(id=diagram_id).count():
            return JsonResponse({"success": False,
                "message": "A diagram with that name already exists"})

        diagram.name = filename
        diagram.diagram = xml
        diagram.save()

        return JsonResponse({"success": True,
            "message": "Diagram saved successfully!"})

@csrf_exempt
def create(request):
    if request.method == "POST":
        filename = unquote(request.POST.get("filename"))
        xml = unquote(request.POST.get("xml"))

        if Diagram.objects.filter(name=filename).count():
            return JsonResponse({"success": False,
                "message": "A diagram with that name already exists"})

        diagram = Diagram(name=filename, diagram=xml)
        diagram.save()

        return JsonResponse({"success": True,
            "message": "Diagram created successfully!",
            "diagram_id": diagram.id})

@csrf_exempt
def rename(request):
    if request.method == "POST":
        new_name = unquote(request.POST.get("new_name"))
        diagram_id = unquote(request.POST.get("diagram_id"))

        try:
            diagram = Diagram.objects.get(id=diagram_id)
        except ObjectDoesNotExist as ex:
            return JsonResponse({"success": False,
                "message": "Diagram does not exist!"})

        if Diagram.objects.filter(name=new_name).exclude(id=diagram_id).count():
            return JsonResponse({"success": False,
                "message": "A diagram with that name already exists"})

        diagram.name = new_name;
        diagram.save()

        return JsonResponse({"success": True,
            "message": "Diagram renamed successfully!"})

@csrf_exempt
def duplicate(request):
    if request.method == "POST":
        new_name = unquote(request.POST.get("new_name"))
        diagram_id = unquote(request.POST.get("diagram_id"))

        try:
            diagram = Diagram.objects.get(id=diagram_id)
        except ObjectDoesNotExist as ex:
            return JsonResponse({"success": False,
                "message": "Diagram does not exist!"})

        if Diagram.objects.filter(name=new_name).count():
            return JsonResponse({"success": False,
                "message": "A diagram with that name already exists"})

        new_diagram = Diagram(name=new_name, diagram=diagram.diagram)
        new_diagram.save()

        return JsonResponse({"success": True,
            "message": "Diagram duplicated successfully!"})

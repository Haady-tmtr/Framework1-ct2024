from django.shortcuts import render, get_object_or_404, redirect
from uo.models import Formation, UE, User
from .forms import UEForm


def menu(request):
    formations = Formation.objects.all()
    return render(request, "uo/menu.html", {"formations" : formations})

def about(request):
    formations = Formation.objects.all()
    return render(request, "uo/about.html", {"formations" : formations})

def details_formation(request, id):
    formation = get_object_or_404(Formation, id=id)
    ues = formation.ues.all()   
    return render(request, "uo/details_formation.html", {"formation" : formation, "ues" : ues})

def details_ue(request, id):
    ue = get_object_or_404(UE, id=id)
    formations = ue.formations.all()
    responsables = ue.responsables.all()
    can_modify = (
        request.user.is_authenticated and (
            any(f.responsable.id == request.user.id for f in formations) or
            request.user in responsables
        )
    )
    return render(request, "uo/details_ue.html", {"ue" : ue, "formations" : formations, "responsables" : responsables, "can_modify": can_modify})

def liste_formation(request):
    formations = Formation.objects.all()
    return render(request, 'uo/liste_formation.html', {'formations' : formations})

def liste_ue(request):
    ues = UE.objects.prefetch_related('formations', 'responsables').all()
    formations = Formation.objects.all()
    return render(request, 'uo/liste_ue.html',{'ues' : ues, 'formations' : formations })



def ajouter_ue(request):
    if request.method == 'POST':
        form = UEForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ues')  
    else:
        form = UEForm()

    return render(request, 'uo/ajouter_ue.html', {'form': form})

def modifier_ue(request, ue_id):
       
    ue = get_object_or_404(UE, pk=ue_id)
    
    if request.method == 'POST':
        form = UEForm(request.POST, instance=ue)
        if form.is_valid():
            form.save()  
            return redirect('details_ue', id=ue.id) 
        form = UEForm(instance=ue)  
    else:
        form = UEForm(instance=ue)

    return render(request, 'uo/modifier_ue.html', {'form': form, 'ue': ue})

def supprimer_ue(request, ue_id):

    ue = get_object_or_404(UE, pk=ue_id)
    
    if request.method == 'POST':
        ue.delete()  
        return redirect('ues')
    return render(request, 'uo/supprimer_ue.html', {'ue': ue})

def resume_formation(request, id):
    formation = get_object_or_404(Formation, id=id)
    ues = formation.ues.all()
    responsables = User.objects.filter(ues_responsables__in=ues).distinct().order_by('last_name', 'first_name')
    h_cms = sum(ue.cm for ue in ues)
    h_tds = sum(ue.td for ue in ues)
    h_tps = sum(ue.tp for ue in ues)

    context = {
        "formation" : formation,
        "ues" : ues,
        "responsables" : responsables,
        "h_cms" : h_cms,
        "h_tds" : h_tds,
        "h_tps" : h_tps,
        "h_total" : (h_cms*1.5 + h_tds + h_tps),
        "total_ects" : sum(ue.credits for ue in ues)
    }
    return render(request, "uo/resume_formation.html", context)

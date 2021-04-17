from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Job
from .models import JobTypes, Cities


# Create your views here.

def joblist(request):
    job_list = Job.objects.order_by('job_type')
    template = loader.get_template('job_list.html')
    context = {'job_list': job_list}
    for job in job_list:
        job.type_name = JobTypes[job.job_type][1]
        job.city_name = Cities[job.job_city][1]
    return HttpResponse(template.render(context))


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404
    return render(request, 'job.html', {'job': job})

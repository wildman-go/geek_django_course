from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Job, Resume
from .models import JobTypes, Cities

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView


# Create your views here.

def joblist(request):
    job_list = Job.objects.order_by('job_type')
    context = {'job_list': job_list}
    for job in job_list:
        job.type_name = JobTypes[job.job_type][1]
        job.city_name = Cities[job.job_city][1]
    return render(request, 'job_list.html', context=context)


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404
    return render(request, 'job.html', {'job': job})


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """创建简历页面"""
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ['username', 'city', 'phone',
              'email', 'apply_position', 'born_address', 'gender',
              'bachelor_school', 'master_school', 'major', 'degree',
              'candidate_introduction', 'work_experience', 'project_experience']

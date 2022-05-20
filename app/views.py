from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from app.services import *
from app.specifications import IsUserAutenticated


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'resumes': ResumeService.get_resumes(not_empty=True)
        }
        return context


class ResumeView(TemplateView):
    template_name = 'resume.html'

    def get(self, request, *args, **kwargs):
        if not IsUserAutenticated(request.user).is_satisfied():
            return HttpResponseRedirect('/')
        return super(ResumeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'resume': ResumeService.get_resume_by_user_id(self.request.user.id),
            'all_languages': LanguageService.get_languages(),
            'all_skills': list({x.value for x in SkillService.get_skills()})
        }
        context['skills'] = SkillService.get_skills_by_resume_id(context['resume'].id)
        context['user_languages'] = [x.language for x in LanguageService.get_user_languages_by_resume_id(
            context['resume'].id)]
        return context

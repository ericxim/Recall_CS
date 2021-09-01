from . models import *
from django.shortcuts import HttpResponseRedirect

class CheckQuestionObjectMixin:
    def dispatch(self, request, *args, **kwargs):
        communities =  self.request.user.communities.all()
        if communities is None:
            return super().dispatch(request, *args, **kwargs)
        for community in communities:
            questions = community.question_set.all()
            for question in questions:
                if QuestionResponse.objects.filter(user=self.request.user, question=question.id):
                    continue
                else:
                    question_obj = Question.objects.get(id=question.id)
                    QuestionResponse.objects.create(user=self.request.user, question=question_obj)
        return super().dispatch(request, *args, **kwargs)

class CheckCommunityAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if Community.objects.filter(id=self.kwargs['pk'], admin=self.request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))
        
class CheckMember:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.communities.filter(id=self.kwargs['pk']).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

class CheckQuestionUser:
    def dispatch(self, request, *args, **kwargs):
        if QuestionResponse.objects.filter(id=self.kwargs['pk'], user=self.request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))
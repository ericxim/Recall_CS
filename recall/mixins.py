from . models import *

class CheckQuestionObjectMixin:
    def dispatch(self, request, *args, **kwargs):
        communities =  self.request.user.communities.all()
        if communities is None:
            return super().dispatch(request, *args, **kwargs)
        for community in communities:
            questions = community.question_set.all()
            for question in questions:
                if QuestionResponse.objects.filter(user=self.request.user, question=question.id):
                    print(QuestionResponse.objects.filter(question = question.id))
                    continue
                else:
                    question_obj = Question.objects.get(id=question.id)
                    QuestionResponse.objects.create(user=self.request.user, question=question_obj)
                    print("Created new object")
        return super().dispatch(request, *args, **kwargs)

class CheckCommunityAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if Community.objects.filter(id=self.kwargs['pk'], admin=self.request.user):
            return super().dispatch(request, *args, **kwargs)
        else:
            print("Not allowed")
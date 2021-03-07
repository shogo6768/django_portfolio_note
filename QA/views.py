from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import QuestionModel, AnswerModel, RequestModel
from accounts.models import CustomUser
from blogs.models import PostModel, Category
from .forms import QuestionForm, AnswerForm, RequestForm



@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionCreate(CreateView):
    template_name = 'QA/questionCreate.html'
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self,  **kwargs):
        return reverse('question_list', kwargs={"pk": 1})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context   

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionList(ListView):
    template_name = 'QA/questionList.html'
    model = QuestionModel

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["questions"] = QuestionModel.objects.all().order_by('-created_at')
        context["pk"] = self.kwargs['pk']
        context["allcats"] = Category.objects.filter(parent=None)
        return context

@login_required(login_url='/accounts/login/')
def questionAnswer(request, pk):
    allcats = Category.objects.filter(parent=None)
    # 質問
    question = get_object_or_404(QuestionModel, pk=pk)
    question.views += 1
    question.save()
    # 回答
    answers = question.answers.all()
    counts = answers.count()
    # 新規回答
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.question = question
            new_answer.created_by = request.user
            new_answer.save()
            return redirect('question_answer', pk=question.pk)
    else:
        answer_form = AnswerForm()

    return render(request, "QA/questionAnswer.html", {
        'allcats':allcats,
        'question': question,
        'answers': answers,
        'form': answer_form,
        'counts': counts
    })

@login_required(login_url='/accounts/login/')
def QuestionRequest(request, pk):
    # allcatsはheaderのためのcontext
    allcats = Category.objects.filter(parent=None)
    question = get_object_or_404(QuestionModel, pk=pk)
    if request.method == 'GET':
        form = RequestForm()
        return render(request, 'QA/questionRequest.html', {'form': form, 'allcats': allcats, 'question': question})
    else:
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request=form.save(commit=False)
            new_request.question=question
            new_request.created_by=request.user
            new_request.save()
            request_subject = form.cleaned_data['subject']
            request_message = form.cleaned_data['message']
            from_email = "no-reply@example.com"
            to_email = QuestionModel.objects.get(pk=pk).created_by.email
            try:
                send_mail(request_subject, request_message,
                          from_email, [to_email])
                messages.success(request, '編集を依頼しました。')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('question_answer', pk=pk)
        return render(request, 'questionRequest.html', {'form': form, 'allcats': allcats, 'question': question})

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionUpdate(UpdateView):
    template_name = 'QA/questionCreate.html'
    model = QuestionModel
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        obj = QuestionModel.objects.get(pk=self.kwargs['pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(QuestionUpdate, self).get(request, *args, **kwargs)

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class AnswerUpdate(UpdateView):
    template_name = 'QA/questionAnswer.html'
    form_class = AnswerForm
    
    def get(self, request, *args, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(AnswerUpdate, self).get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        return obj

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        question = QuestionModel.objects.get(pk=self.kwargs['pk'])
        context["question"] = question
        context["allcats"] = Category.objects.filter(parent=None)
        context["answers"] = AnswerModel.objects.filter(
            question=self.kwargs['pk'])
        context["counts"] = AnswerModel.objects.filter(
            question=self.kwargs['pk']).count()
        return context

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionDelete(DeleteView):
    model = QuestionModel
    template_name = 'QA/delete.html'

    def get(self, request, *args, **kwargs):
        obj = QuestionModel.objects.get(pk=self.kwargs['pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(QuestionDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context
    
    def get_success_url(self,  **kwargs):
        return reverse("question_list", kwargs={"pk": 1})

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class AnswerDelete(DeleteView):
    model = AnswerModel
    template_name = 'QA/delete.html'

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})

    def get_object(self, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        return obj

    def get(self, request, *args, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(AnswerDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context

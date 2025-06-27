from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from .models import Answer, Tag, AnswerTag
from django.shortcuts import render
from .models import Answer


from django.db.models import Count


def answer_list(request):
    answers = Answer.objects.all()

    value = request.GET.get("value")
    lang = request.GET.get("lang")
    type = request.GET.get("type")

    if value:
        answers = answers.filter(value=value)
    if lang:
        answers = answers.filter(language=lang)
    if type:
        answers = answers.filter(type=type)

    answers = answers.annotate(tag_count=Count("answertag"))

    values = Answer.objects.values_list("value", flat=True).distinct()
    languages = Answer.objects.values_list("language", flat=True).distinct()
    types = Answer.objects.values_list("type", flat=True).distinct()

    return render(request, "surveys/answer_list.html", {
        "answers": answers,
        "values": values,
        "languages": languages,
        "types": types,
    })


def answer_detail(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    tags = AnswerTag.objects.filter(answer=answer)

    if request.method == "POST":
        tag_name = request.POST.get("tag_name").strip()
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            AnswerTag.objects.get_or_create(answer=answer, tag=tag)
        return redirect("answer_detail", pk=answer.pk)

    return render(request, "surveys/answer_detail.html", {
        "answer": answer,
        "tags": tags,
    })


def answer_list_for_category(request, value, language, type):
    answers = Answer.objects.filter(
        value=value,
        language=language,
        type=type
    ).annotate(tag_count=Count("answertag"))

    return render(request, "surveys/answer_list.html", {
        "answers": answers,
        "value": value,
        "language": language,
        "type": type,
    })

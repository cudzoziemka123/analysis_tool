from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from .models import Answer, Tag, AnswerTag
from django.shortcuts import render


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

    # Lista istniejących tagów dla tej samej kategorii (value + lang + type)
    existing_tags = Tag.objects.filter(
        answertag__answer__value=answer.value,
        answertag__answer__language=answer.language,
        answertag__answer__type=answer.type
    ).distinct()

    if request.method == "POST":
        if "add_new_tag" in request.POST:
            tag_name = request.POST.get("tag_name").strip()
            category = request.POST.get("category")
            if tag_name:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, defaults={"category": category})
                AnswerTag.objects.get_or_create(answer=answer, tag=tag)
            return redirect("answer_detail", pk=answer.pk)

        if "assign_existing_tag" in request.POST:
            tag_id = request.POST.get("existing_tag")
            tag = Tag.objects.get(id=tag_id)
            AnswerTag.objects.get_or_create(answer=answer, tag=tag)
            return redirect("answer_detail", pk=answer.pk)

        if "delete_tag" in request.POST:
            tag_id = request.POST.get("tag_id")
            AnswerTag.objects.filter(answer=answer, tag_id=tag_id).delete()
            return redirect("answer_detail", pk=answer.pk)

    return render(request, "surveys/answer_detail.html", {
        "answer": answer,
        "tags": tags,
        "existing_tags": existing_tags,
        "CATEGORY_CHOICES": Tag.CATEGORY_CHOICES,


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

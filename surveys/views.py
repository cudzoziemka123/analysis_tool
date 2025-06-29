from collections import defaultdict
import csv
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .models import Answer, Tag, AnswerTag
from .forms import TagForm
from django.core.paginator import Paginator


def answer_list(request):
    value = request.GET.get("value")
    lang = request.GET.get("lang")
    type = request.GET.get("type")

    answers_qs = Answer.objects.all()

    if value:
        answers_qs = answers_qs.filter(value__iexact=value)
    if lang:
        answers_qs = answers_qs.filter(language=lang)
    if type:
        answers_qs = answers_qs.filter(type=type)

    answers_qs = answers_qs.annotate(tag_count=Count("answertag"))

    paginator = Paginator(answers_qs, 30)
    page_number = request.GET.get("page")
    answers = paginator.get_page(page_number)

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

    error_message = None

    if request.method == "POST":
        try:
            if "add_new_tag" in request.POST:
                tag_name = request.POST.get("tag_name", "").strip()
                category = request.POST.get("category")
                if not tag_name:
                    error_message = "Nazwa tagu nie może być pusta."
                else:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name, defaults={"category": category})
                    AnswerTag.objects.get_or_create(answer=answer, tag=tag)
                if not error_message:
                    # Przekieruj z zachowanymi parametrami GET
                    return redirect(f"{request.path}?{request.GET.urlencode()}")

            if "assign_existing_tag" in request.POST:
                tag_id = request.POST.get("existing_tag")
                if not tag_id:
                    error_message = "Nie wybrano istniejącego tagu."
                else:
                    try:
                        tag = Tag.objects.get(id=tag_id)
                        AnswerTag.objects.get_or_create(answer=answer, tag=tag)
                        # Przekieruj z zachowanymi parametrami GET
                        return redirect(f"{request.path}?{request.GET.urlencode()}")
                    except Tag.DoesNotExist:
                        error_message = "Wybrany tag nie istnieje."

            if "delete_tag" in request.POST:
                tag_id = request.POST.get("tag_id")
                if not tag_id:
                    error_message = "Nie wybrano tagu do usunięcia."
                else:
                    deleted, _ = AnswerTag.objects.filter(
                        answer=answer, tag_id=tag_id).delete()
                    if not deleted:
                        error_message = "Nie znaleziono powiązania tagu do usunięcia."
                    else:
                        # Przekieruj z zachowanymi parametrami GET
                        return redirect(f"{request.path}?{request.GET.urlencode()}")
        except Exception as e:
            error_message = f"Wystąpił błąd: {str(e)}"

    return render(request, "surveys/answer_detail.html", {
        "answer": answer,
        "tags": tags,
        "existing_tags": existing_tags,
        "CATEGORY_CHOICES": getattr(Tag, 'CATEGORY_CHOICES', []),
        "error_message": error_message,
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


def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    next_url = request.GET.get('next', 'answer_list')

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            # Sprawdź parametr next z formularza POST, a jeśli nie ma, użyj z GET
            next_url = request.POST.get('next', next_url)
            # Przekieruj do strony, z której przyszedł użytkownik
            return redirect(next_url)
    else:
        form = TagForm(instance=tag)

    return render(request, "surveys/edit_tag.html", {
        "form": form,
        "tag": tag,
        "next_url": next_url
    })


def export_answers_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="tagged_answers.csv"'

    # Ustawiamy kodowanie UTF-8 z BOM, żeby Excel sobie poradził
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Nagłówki
    writer.writerow([
        'ID odpowiedzi',
        'Treść odpowiedzi',
        'Język',
        'Typ',
        'Wartość',
        'Tag',
        'Kategoria tagu'
    ])

    for answertag in AnswerTag.objects.select_related('answer', 'tag'):
        writer.writerow([
            answertag.answer.id,
            answertag.answer.content,
            answertag.answer.language,
            answertag.answer.type,
            answertag.answer.value,
            answertag.tag.name,
            answertag.tag.get_category_display()
        ])

    return response


def analysis_summary(request):
    # Zbieramy dane
    answer_tags = AnswerTag.objects.select_related("answer", "tag")
    data = {}

    for at in answer_tags:
        value = at.answer.value
        langtype = f"{at.answer.language}-{at.answer.type}"
        category = at.tag.category
        tag_name = at.tag.name

        if not (value and langtype and category and tag_name):
            continue

        # Inicjalizacje zagnieżdżonych słowników
        data.setdefault(value, {}).setdefault(
            langtype, {}).setdefault(category, {})

        # Zliczanie wystąpień tagów
        data[value][langtype][category][tag_name] = data[value][langtype][category].get(
            tag_name, 0) + 1

    return render(request, "surveys/analysis_summary.html", {"data": data})

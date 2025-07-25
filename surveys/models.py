from django.db import models


class Answer(models.Model):
    LANGUAGE_CHOICES = [
        ('pl', 'Polski'),
        ('ua', 'Ukraiński'),
    ]
    TYPE_CHOICES = [
        ('skojarzenie', 'Skojarzenie'),
        ('definicja', 'Definicja'),
    ]

    value = models.CharField(max_length=100)  # Np. 'MIŁOŚĆ', 'SPRAWIEDLIWOŚĆ'
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    content = models.TextField()  # Treść odpowiedzi z ankiety

    def __str__(self):
        return f"[{self.value} - {self.language}] {self.content[:40]}"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    language = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    CATEGORY_CHOICES = [
        ("definition", "Określenie"),
        ("object", "Obiekt"),
        ("notion", "Pojęcie"),
        ("experience", "Doznanie"),
        ("action", "Działanie"),
        ("attributes", "Atrybut"),
    ]
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="pojęcie")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        unique_together = ('name', 'value', 'language', 'type')


class AnswerTag(models.Model):
    answer = models.ForeignKey(
        Answer, related_name='answertag', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.answer} → {self.tag}"

    class Meta:
        # Zapobiega duplikowaniu tych samych tagów
        unique_together = ('answer', 'tag')

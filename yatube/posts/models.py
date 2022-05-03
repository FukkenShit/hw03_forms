from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True,
        help_text='Уникальный идентификатор сообщества.'
    )
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст записи',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Сообщество',
        help_text='Сообщество, к которому относится запись',
    )

    class Meta:
        ordering = ('-pub_date',)

    @property
    def short_text(self):
        """Обрезанный текст поста для показа в админке."""
        MAX_LENGTH = 50
        return self.text if len(self.text) <= MAX_LENGTH else self.text[:MAX_LENGTH] + '...'

    def __str__(self) -> str:
        return f'{self.pk}\t[Автор: {self.author}]\t[Сообщество: {self.group}]\t[{self.short_text}]'

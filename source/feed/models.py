from django.db import models

from accounts.models import Profile

class Category(models.Model):
    title = models.CharField('Название', max_length=150)

    def __str__(self):
        return f'{self.title}'


class PostModel(models.Model):
    MOD_CHOICES = (
        ('M', 'Опубликовано'),
        ('W', 'На модерации'),
        ('U', 'Отклонено'),
        ('D', 'На удаление')
    )

    image = models.ImageField('Картинка', upload_to='post_images', null=True, blank=True)
    author = models.ForeignKey(Profile, verbose_name='Пользователь', related_name='usr_posts', on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст публикации', max_length=1000)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='pCategory', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('Цена', default=1)
    moderate = models.CharField('Модерация', max_length=1, blank=False, null=True, choices=MOD_CHOICES, default='W')
    date_add = models.DateTimeField('Дата публикации', auto_now_add=True)
    date_edit = models.DateTimeField('Дата редактирования', auto_now=True)
    date_moderate = models.DateTimeField('Дата публикации', null=True, blank=True)
    

class CommentModel(models.Model):
    author = models.ForeignKey(Profile, verbose_name='Пользователь', related_name='a_comment', on_delete=models.SET_NULL, blank=True, null=True)
    post_model = models.ForeignKey(PostModel, verbose_name='Продукт', related_name='p_comment', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField('Текст комментария', max_length=1500)
    date_add = models.DateField('Дата публикации', auto_now_add=True)
    date_edit = models.DateField('Дата редактирования', auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_author(self):
        return Profile.objects.get(username=self.author)
    
    def get_product(self):
        return PostModel.objects.get(id=self.post_model)


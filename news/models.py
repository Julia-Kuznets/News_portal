from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей автора * 3
        post_rating = self.post_set.aggregate(pr=Sum('rating'))['pr'] or 0
        post_rating *= 3

        # Суммарный рейтинг комментариев автора
        comment_rating = self.user.comment_set.aggregate(cr=Sum('rating'))['cr'] or 0

        # Суммарный рейтинг комментариев к статьям автора (ИСПРАВЛЕННАЯ ВЕРСИЯ)
        post_comment_rating = (
                Comment.objects
                .filter(related_post__in=self.post_set.all())
                .aggregate(pcr=Sum('rating'))['pcr'] or 0
        )

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    NEWS = 1
    ARTICLE = 2
    POST_TYPES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.IntegerField(choices=POST_TYPES, default=NEWS, verbose_name='Тип поста')
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='Postcategory')
    title = models.CharField(max_length=200)
    post_content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_content[:124] + '...' if len(self.post_content) > 124 else self.post_content

    def __str__(self):
        return f"{self.title} (by {self.author.user.username})"


class Postcategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comm_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.comm_text
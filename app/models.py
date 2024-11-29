from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Categories(models.Model):
    icon = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    def category(self):
        return Categories.objects.all().order_by('id')

class Author(models.Model):
    author_profile=models.ImageField(upload_to='media/author')
    author_name=models.CharField(max_length=100)
    about_author=models.TextField()

    def __str__(self):
        return self.author_name

class Level(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    language=models.CharField(max_length=100,default="English")

    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS=(("PUBLISH","PUBLISH"),("DRAFT","DRAFT"),)
    featured_image=models.ImageField(upload_to="media/featured_img")
    featured_video=models.CharField(max_length=300)
    title=models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,)
    level= models.ForeignKey(Level,on_delete=models.CASCADE,default="")
    description=models.TextField()
    price=models.FloatField()
    discount=models.FloatField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE,null=True)
    deadline=models.CharField(max_length=100,null=True)
    slug = models.SlugField(default='', max_length=100, blank=True)
    status = models.CharField(choices=STATUS, max_length=100)
    certificate = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title

    def course(self):
        return Course.objects.filter(status='PUBLISH')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug':self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class What_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    point = models.CharField(max_length=500)

    def __str__(self):
        return self.point

class Requirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    point = models.CharField(max_length=500)

    def __str__(self):
        return self.point

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="media/Yt_thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    youtube_id = models.CharField(max_length=500)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class UserCourse(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    paid=models.BooleanField(default=0)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name+"-"+self.course.title

class Payment(models.Model):
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " -- " + self.course.title


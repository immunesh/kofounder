from django.db import models

class Category(models.Model):
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, help_text='Upload an image to feature for this category.')
    title = models.CharField(max_length=100, blank=True, null=True, help_text='Title for display in blog page')
    name = models.CharField(max_length=100, db_index=True, help_text='Name of the category.')
    slug = models.SlugField(unique=True, db_index=True, help_text='URL-friendly identifier for the category.')
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    tags = models.ManyToManyField(Tag)
    featured_image = models.ImageField(upload_to='blog/post_images/')
    views_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = self.content[:100]
        super().save(*args, **kwargs)
    
    def get_related_posts(self):
        related_posts = Post.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct()[:5]
        return related_posts

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    # image = models.ImageField(blank=True)
    
    def __str__(self):
        return self.content
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
            upload_to='posts/images',							# 저장 위치
            processors=[ResizeToFill(600, 600)],		# 처리할 작업 목록
            format='JPEG',													# 저장 포맷
            options={'quality': 90},								# 옵션
				)
				
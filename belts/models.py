from django.db import models

class Belt(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Orange, Brown 3, Black 1")
    display_order = models.IntegerField(unique=True, help_text="Logical order for sorting belts.")
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, help_text="The PDF manual for this belt.")

    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return self.name
    
class Technique(models.Model):
    belt = models.ForeignKey(Belt, related_name='techniques', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    order_in_belt = models.IntegerField(help_text="The sequential order of the technique within the belt.")

    class Meta:
        ordering = ['belt__display_order', 'order_in_belt']
        unique_together = ('belt', 'order_in_belt') # Ensure order is unique per belt
    
    def __str__(self):
        return f"{self.belt.name}: {self.name}"
    
    def get_video_url(self):
        """Helper method to safely return the video URL."""
        if self.video_file and hasattr(self.video_file, 'url'):
            return self.video_file.url
        return None
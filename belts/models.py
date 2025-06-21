from django.db import models

class BeltGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_order = models.IntegerField(unique=True, help_text="Order in which groups appear on the dashboard.")
    color = models.CharField(max_length=7, default='#696969', help_text="Hex color code for the group's folder (e.g., #696969).")

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name

class Belt(models.Model):
    group = models.ForeignKey(BeltGroup, related_name='belts', on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional group this belt belongs to.")
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Orange, Brown 3, Black 1")
    display_order = models.IntegerField(unique=True, help_text="Logical order for sorting belts.")
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, help_text="The PDF manual for this belt.")
    color = models.CharField(max_length=7, default='#B48A3A', help_text="Hex color code for the belt (e.g., #FFFFFF).")

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
    video_enabled = models.BooleanField(default=False, help_text="Show video player/placeholder on the technique page.")

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
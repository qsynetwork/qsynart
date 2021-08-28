import random

from django.db import models
from multiselectfield import MultiSelectField


class Artists(models.Model):
    name = models.CharField(max_length=200, null=True)
    profile_picture = models.FileField(null=True, default="default_pic.jpg")
    about = models.TextField(null=True,blank=True)
    facebook_link = models.CharField(max_length=200, null=True, blank=True, default="")
    instagram_link = models.CharField(max_length=200, null=True, blank=True, default="")
    instagram_link2 = models.CharField(max_length=200, null=True, blank=True, default="")
    linkedin_link = models.CharField(max_length=200, null=True, blank=True, default="")
    youtube_link = models.CharField(max_length=200, null=True, blank=True, default="")
    email_address = models.CharField(max_length=200, null=True, blank=True, default="")
    custom_link_1 = models.CharField(max_length=200, null=True, blank=True, default="")
    custom_link_2 = models.CharField(max_length=200, null=True, blank=True, default="")

    def __str__(self):
        return self.name

SIZE_CHOICES = (
    (2,"10x10"),
    (3,"20x20"),
    (4,"29x14.5"),
    (5,"42x21"),
    (6,"A3"),
    (7,"A4"),
    (8,"A5"),
    # (9,"A6")
)

class Artwork(models.Model):
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE, related_name="artwork_of_artist")
    picture = models.FileField(null=True)
    sizes_available = MultiSelectField(choices=SIZE_CHOICES,null=True)


class ArtworkSize(models.Model):
    size = models.CharField(max_length=50, null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.size} =>  ₹ {self.price}"


class OrderHistory(models.Model):
    order_id = models.CharField(max_length=50, null=True, default="")
    order_details = models.JSONField(null=True, default=dict)
    ketto_transaction_details = models.FileField(null=True)
    total_price = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=100, null=True)
    customer_email = models.CharField(max_length=50, null=True)
    customer_phoneNo = models.CharField(max_length=60, null=True)
    customer_address = models.TextField(null=True)
    customer_pinCode = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        run = True
        while run:
            unique_order_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            if len(OrderHistory.objects.filter(order_id=unique_order_id)) != 0:
                continue
            self.order_id = unique_order_id
            run = False
        super(OrderHistory, self).save(*args, **kwargs)

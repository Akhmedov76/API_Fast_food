from django.db import models

class MenuItemModel(models.Model):
    """
    MenuItemModel is a model to represent the menu items available in the restaurant.
    It has fields such as name, price, description, is_available, created_at, and updated_at.
    The name field is a CharField with a maximum length of 255 characters.
    The price field is a DecimalField with a maximum of 6 digits and 2 decimal places.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

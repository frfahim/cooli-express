from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProductTypes(TextChoices):
    BOOKS = 'books', _('Books')
    BEAUTY_ACCESSORIES = 'beauty_accessories', _('Beauty Accessories')
    CLOTHING = 'clothing', _('Clothing')
    CRAFTS = 'crafts', _('Crafts')
    DOCUMENT = 'documents', _('Documents')
    ELECTRONICS = "electronics", _('Electronics')
    FOOD = "food", _('Food')
    FISH = "fish", _('Fish')
    FASHION_ACCESSORIES = "fashion_accessories", _('Fashion Accessories')
    GROCERY = "grocery", _('Grocery')
    HOME_DECOR = "home_decor", _('Home Decor')
    JEWELLERY = "jewellery", _('Jewellery')
    FRAGILE_ITEM = "fragile_item", _('Fragile Item')
    OTHERS = "others", _('Others')


class OrderStatus(TextChoices):
    PENDING = 'pending', _('Pending')
    # PROCESSING = 'processing', _('Processing')
    ACCEPTED = 'accepted', _('Accepted')
    REJECTED = 'rejected', _('Rejected')
    PICKED = 'picked', _('Picked')
    IN_HUB = 'in_hub', _('In Hub')
    ON_THE_WAY = 'on_the_way', _('On the Way')
    DELIVERED = 'delivered', _('Delivered')

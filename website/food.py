from django.db import models
from django.shortcuts import render, redirect
from .models import FoodCategory, FoodItem, Order

class FoodCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food_images/', blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    room_number = models.IntegerField()
    food_items = models.ManyToManyField(FoodItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.customer_name} in room {self.room_number}"

def food_menu(request):
    food_categories = FoodCategory.objects.all()
    food_items = FoodItem.objects.all()
    context = {'food_categories': food_categories, 'food_items': food_items}
    return render(request, 'food/menu.html', context)

def food_item_detail(request, pk):
    food_item = FoodItem.objects.get(pk=pk)
    context = {'food_item': food_item}
    return render(request, 'food/item_detail.html', context)

def create_order(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        room_number = request.POST['room_number']
        selected_food_items = request.POST.getlist('food_items')

        food_items = FoodItem.objects.filter(pk__in=selected_food_items)
        total_price = sum(item.price for item in food_items)

        order = Order.objects.create(
            customer_name=customer_name,
            room_number=room_number,
            food_items=food_items,
            total_price=total_price
        )

        return redirect('food_menu')

    food_categories = FoodCategory.objects.all()
    food_items = FoodItem.objects.all()
    context = {'food_categories': food_categories, 'food_items': food_items}
    return render(request, 'food/create_order.html', context)

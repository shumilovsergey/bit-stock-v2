# [modells up]
from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict)  # Use default=dict to start with an empty dictionary

    def __str__(self):
        return self.name
    

# [creating]

#from myapp.models import Categories

# Create a new instance with nested data
data = {
    "Apple": ["MacBook", "iPhone"],
    "Asus": ["Inspire", "Inspire-2"],
    "Samsung": ["laptop", "phone"]
}

category = Categories.objects.create(name='Electronics', data=data)
print(category.data)  # Output: {'Apple': ['MacBook', 'iPhone'], 'Asus': ['Inspire', 'Inspire-2'], 'Samsung': ['laptop', 'phone']}


#  [up dating model]

# Fetch an existing instance
category = Categories.objects.get(id=1)

# Update the nested data
category.data["Apple"].append("iPad")
category.save()

print(category.data)  # Output: {'Apple': ['MacBook', 'iPhone', 'iPad'], 'Asus': ['Inspire', 'Inspire-2'], 'Samsung': ['laptop', 'phone']}

# [admin setting]

from django.contrib import admin
from .models import Categories

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'data')


#  [add brand + products]

#from myapp.models import Categories

# Create a new instance with an empty list for Lenovo
new_category = Categories.objects.create(name='Electronics', data={'Lenovo': []})

print(new_category.data)  # Output: {'Lenovo': []}



# Fetch the existing instance for Lenovo
category_lenovo = Categories.objects.get(name='Electronics')

# Update the list of models for Lenovo
category_lenovo.data['Lenovo'] = ['ThinkPad', 'Yoga', 'IdeaPad']

# Save the changes
category_lenovo.save()

print(category_lenovo.data)  # Output: {'Lenovo': ['ThinkPad', 'Yoga', 'IdeaPad']}


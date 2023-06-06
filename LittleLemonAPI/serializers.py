from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured']

    def create(self, validated_data):
        category_id = validated_data.pop('category').id
        menu_item = MenuItem.objects.create(category_id=category_id, **validated_data)
        return menu_item


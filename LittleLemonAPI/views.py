from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem,Category
from .serializers import  MenuItemSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User , Group
# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingletMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        # filtering  
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        # searching
        search = request.query_params.get('search')
        # ordering
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default =2)
        page = request.query_params.get('page',default =1)
        if category_name:
            items = items.filter(category=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__istartswith=search)
        if ordering:
            # items = items.order_by(ordering)  
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
            paginator = Paginator(items, per_page= perpage)
            try:
                items = paginator.page(number=page)
            except EmptyPage:
                items = []   
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == 'POST':
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status=status.HTTP_201_CREATED)
    
    
@api_view()
def single_items(request,id):
    items = get_object_or_404(MenuItem, pk=id)
    serialized_items = MenuItemSerializer(items)
    return Response(serialized_items.data)  


   
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"some authentication required"})    

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
       return Response({"only manager is allowed to see this"}) 
    else:
     return Response({"message":"you are not authorized"},403)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User,username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method =='DELETE':
              managers.user_set.remove(user)
        return Response({"message":"OK"}) 
    return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)           

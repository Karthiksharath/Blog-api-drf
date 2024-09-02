from rest_framework.views import APIView
from .serializers import BlogSerializer
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication



class PublicBlogView(APIView):

  def get(self,request):

    try:
      
      blogs = Blog.objects.all().order_by('?')

      if request.GET.get('search'):

        search = request.GET.get('search')

        blogs = Blog.objects.filter(Q(title__icontains = search)| (Q(blog_text__icontains = search)))


      page_number = request.GET.get('page', 5)

      paginator = Paginator(blogs, 1)

      serializer = BlogSerializer(paginator.page(page_number), many=True)

      return Response({'data':serializer.data,
                       'message':'blogs fetched successfully..'},status=status.HTTP_201_CREATED)
    
    except Exception as e:

      return Response({'data':{},
                       'message':'invakid page or something wrong..'},status=status.HTTP_400_BAD_REQUEST)


class BlogView(APIView):

  permission_classes = [IsAuthenticated]

  authentication_classes = [JWTAuthentication]

  def get(self,request):

    try:
      
      blogs = Blog.objects.filter(user = request.user)

      if request.GET.get('search'):

        search = request.GET.get('search')

        blogs = Blog.objects.filter(Q(title__icontains = search)| (Q(blog_text__icontains = search)))


      serializer = BlogSerializer(blogs, many=True)

      return Response({'data':serializer.data,
                       'message':'blogs fetched successfully..'})
    
    except Exception as e:
      pass

  def post(self, request):

    try:

      data = request.data

      data['user'] = request.user.id

      serializer = BlogSerializer(data=data)

      if not serializer.is_valid():

        return Response({"errors":serializer.errors,
                  'message':"something is wrong"},status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save() 

      return Response({"data":serializer.data,
                  'message':"blog created"},status=status.HTTP_201_CREATED)      

    
    except Exception as e:

      print(e)

      return Response({"message":"something is wrong"})

  
  def patch(self, request):

    try:

      data = request.data

      blog = Blog.objects.filter(uid = data.get('uid'))

      if not blog.exists():

        return Response({"message":"blog doesnot exists"}, status=status.HTTP_400_BAD_REQUEST)

      if request.user != blog[0].user:

        return Response({'message':'you are not authorized'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

      serializer = BlogSerializer( blog[0],data=data, partial = True)

      if not serializer.is_valid():

        return Response({'data':serializer.errors,
                         'message':"blog updated successfully.."},status=status.HTTP_201_CREATED)
      
      serializer.save()

      return Response({"data":serializer.data,
                      'message':"blog created"}
                      ,status=status.HTTP_201_CREATED)      


    except Exception as e:

      print(e)


  def delete(self, request):

    try:

      data = request.data

      blog = Blog.objects.filter(uid = data.get('uid'))

      if not blog.exists():

        return Response({"message":"invalid uid"}, status=status.HTTP_400_BAD_REQUEST)

      if request.user != blog[0].user:

        return Response({'message':'you are not authorized'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
      
      blog[0].delete()

      return Response({"data":{},
                      'message':"blog deleted"}
                      ,status=status.HTTP_200_OK)  

    except Exception as e:

      print(e)

  



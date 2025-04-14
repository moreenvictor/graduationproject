from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Material, RecycleBag, Notification, UserProfile
from .serializers import NotificationSerializer, RecycleBagSerializer, UserProfileSerializer
from .notifications import send_notification  # تأكد من أن الاستيراد صحيح
from .models import RecycledItem
from .serializers import RecycledItemSerializer

class ItemList(APIView):
    def get(self, request):
        items = RecycledItem.objects.all()
        serializer = RecycledItemSerializer(items, many=True)
        return Response(serializer.data)


class RecycleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user  # التأكد من استخدام request.user
        material_id = request.data.get('material_id')
        count = request.data.get('count', 1)  # استخدام count بدلاً من points

        try:
            material = Material.objects.get(id=material_id)
        except Material.DoesNotExist:
            return Response({'error': 'المادة غير موجودة'}, status=status.HTTP_404_NOT_FOUND)

        # إذا لم يكن الـ UserProfile موجود، سيتم إنشاؤه هنا
        profile, created = UserProfile.objects.get_or_create(user=user)

        # إنشاء RecycleBag جديد
        recycle = RecycleBag.objects.create(user=user, material=material, points=count)

        # تحديث نقاط المستخدم
        profile.points += count
        profile.save()

        # حفظ الإشعار في قاعدة البيانات
        title = "شكراً لإعادة التدوير!"
        message = f"لقد حصلت على {count} نقطة عند إعادة تدوير {material.name}."
        Notification.objects.create(user=user, title=title, message=message)

        # إرسال إشعار عبر FCM
        send_notification(user, title, message)

        return Response({
            'message': 'تمت إضافة العملية وحساب النقاط بنجاح',
            'current_points': profile.points
        }, status=status.HTTP_201_CREATED)



class NotificationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-date_created')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MarkNotificationAsRead(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "تم تحديث الإشعار إلى مقروء"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "الإشعار غير موجود"}, status=status.HTTP_404_NOT_FOUND)



class RecycleBagView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recycle_bag = RecycleBag.objects.filter(user=request.user)
        serializer = RecycleBagSerializer(recycle_bag, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        profile = request.user.userprofile  # استخدم request.user بدلاً من user
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'تم التحديث بنجاح'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



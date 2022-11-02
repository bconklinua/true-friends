from rest_framework import serializers, viewsets, status, permissions, response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ..User.models import Author
from .models import Follow


class FollowersListView(GenericAPIView):
    def get(self, request):
        if not Author.objects.filter(username=request.user.username).exists():
            return response.Response({"error": "invalid author object"}, status=status.HTTP_400_BAD_REQUEST)
        author = Author.objects.get(username=request.user.username).id
        follower_list = Follow.objects.filter(followee=author)

        f_list = []
        for f in follower_list:
            f_dict = {}
            f_id = f.id
            sender = Author.objects.get(id=f.follower.id)
            sender_id = f.follower.id
            sender_username = sender.username
            sender_first_name = sender.first_name
            sender_last_name = sender.last_name
            sender_email = sender.email
            f_date = f.date
            f_dict.update({'id:': f_id})
            f_dict.update({'date': f_date})
            f_dict.update({'sender_id': sender_id})
            f_dict.update({'sender_username': sender_username})
            f_dict.update({'sender_email': sender_email})
            f_dict.update({'sender_first_name': sender_first_name})
            f_dict.update({'sender_last_name': sender_last_name})

            f_list.append(f_dict)

        return response.Response(f_list, status=status.HTTP_200_OK)


class TrueFriendsListView(GenericAPIView):
    def get(self, request):
        if not Author.objects.filter(username=request.user.username).exists():
            return response.Response({"error": "invalid author object"}, status=status.HTTP_400_BAD_REQUEST)
        author = Author.objects.get(username=request.user.username).id
        follower_list = Follow.objects.filter(followee=author)

        f_list = []
        for f in follower_list:
            f_id = f.id
            sender = Author.objects.get(id=f.follower.id)
            follow_back = Follow.objects.filter(followee=sender.id, follower=author)
            if len(follow_back) > 0:
                tf_dict = {}
                tf_id = f.follower.id
                tf_username = sender.username
                tf_first_name = sender.first_name
                tf_last_name = sender.last_name
                tf_email = sender.email
                f_date = f.date
                tf_dict.update({'id:': f_id})
                tf_dict.update({'date': f_date})
                tf_dict.update({'friend_id': tf_id})
                tf_dict.update({'friend_username': tf_username})
                tf_dict.update({'friend_email': tf_email})
                tf_dict.update({'friend_first_name': tf_first_name})
                tf_dict.update({'friend_last_name': tf_last_name})
                f_list.append(tf_dict)

        return response.Response(f_list, status=status.HTTP_200_OK)

class FollowingListView(GenericAPIView):
    def get(self, request):
        if not Author.objects.filter(username=request.user.username).exists():
            return response.Response({"error": "invalid author object"}, status=status.HTTP_400_BAD_REQUEST)
        author = Author.objects.get(username=request.user.username).id
        follower_list = Follow.objects.filter(follower=author)

        f_list = []
        for f in follower_list:
            f_dict = {}
            f_id = f.id
            recipient = Author.objects.get(id=f.followee.id)
            recipient_id = f.followee.id
            recipient_username = recipient.username
            recipient_email = recipient.email
            recipient_first_name = recipient.first_name
            recipient_last_name = recipient.last_name
            f_date = f.date
            f_dict.update({'id:': f_id})
            f_dict.update({'date': f_date})
            f_dict.update({'recipient_id': recipient_id})
            f_dict.update({'recipient_username': recipient_username})
            f_dict.update({'recipient_email': recipient_email})
            f_dict.update({'recipient_first_name': recipient_first_name})
            f_dict.update({'recipient_last_name': recipient_last_name})

            f_list.append(f_dict)

        return response.Response(f_list, status=status.HTTP_200_OK)


class UnfollowView(GenericAPIView):

    def post(self, request, user_id):
        user_id = self.kwargs['user_id']
        user_obj = Author.objects.get(id=user_id)
        name = user_obj.username
        if not Follow.objects.filter(follower=request.user.id, followee=user_obj.id).exists():
            return response.Response({"error": "invalid follow object - you are not following a user with that id"},
                                     status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.filter(follower=request.user.id, followee=user_obj.id).delete()
        msg_str = name + " has been unfollowed."
        message = {"message": msg_str}
        return response.Response(message, status=status.HTTP_200_OK)
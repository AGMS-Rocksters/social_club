from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from posts.models import Post, Comment
from rest_framework_simplejwt.tokens import RefreshToken


class PostTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Create test post
        self.post = Post.objects.create(
            user=self.user, title="Test Post", description="This is a test post"
        )
        # URLs to access the post list and detail
        self.post_list_url = reverse("posts:post-list")
        self.post_detail_url = reverse("posts:post-detail", args=[self.post.id])

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def set_jwt_authentication(self):
        jwt_token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token)

    def test_post_list(self):
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_detail(self):
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")

    def test_create_post(self):
        self.set_jwt_authentication()
        data = {"title": "New Post", "description": "Description of the new post"}
        response = self.client.post(self.post_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_update_post(self):
        self.set_jwt_authentication()
        data = {"title": "Updated Post", "description": "Updated description"}
        response = self.client.put(self.post_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post.id).title, "Updated Post")

    def test_delete_post(self):
        self.set_jwt_authentication()
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)


class CommentTests(APITestCase):
    def setUp(self):
        # Create test user and post
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.post = Post.objects.create(
            user=self.user, title="Test Post", description="This is a test post"
        )
        self.comment = Comment.objects.create(
            user=self.user, post=self.post, content="This is a comment"
        )

        self.comment_list_url = reverse("posts:comment-list", args=[self.post.id])
        self.comment_detail_url = reverse(
            "posts:comment-detail", args=[self.post.id, self.comment.id]
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def set_jwt_authentication(self):
        jwt_token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token)

    def test_comment_list(self):
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_comment_detail(self):
        response = self.client.get(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "This is a comment")

    def test_create_comment(self):
        self.set_jwt_authentication()
        data = {"content": "New comment", "post": self.post.id}

        response = self.client.post(self.comment_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_update_comment(self):
        self.set_jwt_authentication()

        data = {"content": "Updated comment", "post": self.post.id}

        response = self.client.put(self.comment_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.content, "Updated comment")

    def test_delete_comment(self):
        self.set_jwt_authentication()
        response = self.client.delete(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

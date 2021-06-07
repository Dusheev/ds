from rest_framework import serializers
from django.contrib.auth.models import User

from blog_app.models import Post, Category


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'password', 'password2', 'email',
        )

    def validated_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Name must start with upper register!")
        return value


    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('ПАРОЛЬ НЕ СОВПАДАЕТ')
        return attrs

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('ПАРОЛЬ НЕ СОВПАДАЕТ')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation



class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'owner', 'comments', 'category', 'preview', 'images')

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        request = self.context.get('request')
        # print("Файлы: ", request.FILES)
        images_data = request.FILES
        created_post = Post.objects.create(**validated_data)
        print(created_post)
        # for image_data in images_data.getlist('image'):
        #     PostImages.objects.create(post=created_post, image=image_data)

        return created_post

        # return super().create(validated_data)

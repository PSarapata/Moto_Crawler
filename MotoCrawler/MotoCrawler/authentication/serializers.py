from rest_framework import serializers
from authentication.models import MotoCrawlerUser


class MotoCrawlerUserSerializer(serializers.ModelSerializer):
    """Custom serializer for our Users. Password is in write-only mode, it will not be displayed.
    It uses a custom create method, creates User object using validated data except password,
    which is being passed after to the set_password method executed on newly created User instance.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = MotoCrawlerUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            user.set_password(password)
        user.save()
        return user

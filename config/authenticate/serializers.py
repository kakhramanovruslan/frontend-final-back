from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .exceptions import UserNotActive, UserNotFound, UserCredentialsError
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email, password = attrs['email'], attrs['password']

        user = User.objects.filter(email=email).first()

        if user is not None:
            if not user.is_active:
                raise UserNotActive

            try:
                return super().validate(attrs)
            except AuthenticationFailed:
                raise UserCredentialsError
        else:
            raise UserNotFound


class UserSerializer(serializers.ModelSerializer):
    id_card_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'iin', 'id_card_image', 'is_superuser')

    def get_id_card_image(self, obj):
        request = self.context.get('request')
        id_card_image = obj.id_card_image.url
        return request.build_absolute_uri(id_card_image)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'iin', 'id_card_image')
        extra_kwargs = {
            'email': {'read_only': True}
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'password',
                  'first_name',
                  'last_name',
                  'phone',
                  'iin',
                  'id_card_image')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            iin=validated_data['iin'],
            id_card_image=validated_data['id_card_image'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SendResetPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserCheckResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

from rest_framework import serializers
from ..models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True,)
    class Meta:
        model = User
        fields = ["username","email","password","confirm_password","role"]
        extra_kwargs = {
            "password":{"write_only":True},
            "role":{"read_only": True},
            "email":{"required": True}
        }
    
    def validate(self,validattion_data):
        

        if validattion_data.get("password") != validattion_data.get("confirm_password"):
            raise serializers.ValidationError({"Password_error":"confirm_password and password must be same "})
        
        if validattion_data.get("email") and User.objects.filter(email=validattion_data["email"]).exists():
            raise serializers.ValidationError(
                {"email_error": "Email already registered"}
            )
        
        return validattion_data
    
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")  
        user = User.objects.create_user(**validated_data)  
        return user
        

class LoginSerializer(serializers.Serializer):
    password=serializers.CharField(write_only=True)
    username=serializers.CharField(write_only=True)

    def validate(self,data):
        username=data.get("username")
        password=data.get("password")
        
        user=authenticate(username=username,password=password)
        
        if not user:
            raise serializers.ValidationError({"error":'invalid email or password'})
        
        refresh = RefreshToken.for_user(user)
        


        return (
        {
            'message':"login succesful",
            "user":{
                "user_id":user.id,
                "username":user.username,
                "email":user.email,
                'role':user.role
            },
            "refresh_token":str(refresh),
            "access_token":str(refresh.access_token)

        }
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email","role"] 
    
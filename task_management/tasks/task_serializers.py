from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields='__all__'

    def validate(self,validation_data):
        status = validation_data.get('status')
        report = validation_data.get('completion_report')
        hours = validation_data.get('worked_hours')

        if status == "completed":
            if not report:
                raise serializers.ValidationError("report is required for mark complete")
            if hours is None:
                raise serializers.ValidationError('worked hours is required for mark complete ')
        return validation_data



class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model =Task
        fields=['status','worked_hours','completion_report']


    def validate(self,data):
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError("completion report is required")
            if data.get('worked_hours') is None:
                raise serializers.ValidationError("worked hours required")
        return data

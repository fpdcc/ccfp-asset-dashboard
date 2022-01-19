from django.contrib.auth.models import User
from rest_framework import serializers

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'category', 'section_owner',)


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ('id',)


class PortfolioPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioPhase
        fields = ('phase', 'sequence',)


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'user', 'created_at', 'updated_at', 'phases',)

    phases = PortfolioPhaseSerializer(many=True, read_only=False)

    def create(self, validated_data):
        phase_data = validated_data.pop('phases')

        portfolio = Portfolio.objects.create(**validated_data)

        for phase in phase_data:
            PortfolioPhase.objects.create(
                portfolio=portfolio,
                phase=phase['phase'],
                sequence=phase['sequence']
            )

        return portfolio

    def update(self, validated_data):
        ...

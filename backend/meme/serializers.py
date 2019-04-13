from rest_framework import serializers

from meme.models import Video, Ranking


class VideoSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)
    quality = serializers.FloatField(default=0.0)
    views = serializers.IntegerField(default=0)
    length = serializers.IntegerField()

    def create(self, validated_data):
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.url = instance.url
        tmp = 1  # TODO open.cv
        instance.quality = (validated_data.get('quality', instance.quality) * instance.views + tmp) / (
                    instance.views + 1)
        # instance.views = validated_data.get('views', instance.views)
        instance.views = instance.views + 1
        instance.length = instance.length
        instance.save()
        return instance


class RankingSerializer(serializers.Serializer):
    video = VideoSerializer()
    position = serializers.IntegerField()

    def create(self, validated_data):
        video_data = validated_data.pop('video', None)
        if video_data:
            video = Video.objects.get_or_create(**video_data)[0]
            validated_data['video'] = video
        return Ranking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.video = validated_data.get('video', instance.video)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        return instance

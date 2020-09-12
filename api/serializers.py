from .models import Vote, Politician, Poll, PollResult
from rest_framework import serializers



class VoteSerializer(serializers.HyperlinkedModelSerializer):
    politician = serializers.HyperlinkedRelatedField(view_name='politician-detail', read_only=True)
    poll = serializers.CharField(read_only=True)
    abg_data = serializers.CharField(source='self.abgeordnetenwatch_data', read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'

    
class PoliticianSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(read_only=True)
    occupation = serializers.CharField(read_only=True)
    party = serializers.CharField(read_only=True)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = '__all__'

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    yes = serializers.IntegerField(read_only=True)
    no = serializers.IntegerField(read_only=True)
    abstain = serializers.IntegerField(read_only=True)
    no_show = serializers.IntegerField(read_only=True)
    result = serializers.CharField(read_only=True)

    class Meta:
        model = PollResult
        fields = '__all__'
        depth = 1

class PollSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(required=False)
    abstract = serializers.CharField(required=False)
    yes = serializers.IntegerField(required=False)
    no = serializers.IntegerField(required=False)
    abstain = serializers.IntegerField(required=False)
    no_show = serializers.IntegerField(required=False)
    result = serializers.CharField(required=False)
    abgeordnetenwatch_id = serializers.IntegerField()
    abgeordnetenwatch_url = serializers.URLField()


    class Meta:
        model = Poll
        fields = '__all__'

    """ def save(self):
        abgeordnetenwatch_id = self.validated_data['abgeordnetenwatch_id']
        abgeordnetenwatch_url = self.validated_data['abgeordnetenwatch_url']
        if PollSerializer(self.validated_data).is_valid():
            return 
        #result = self.validated_data['result'] """

    """  def create(self, validated_data):
        print('\nValidated Data:')
        print(validated_data)
        result_data = validated_data.pop('result')
        poll = Poll.objects.create(**validated_data)
        PollResult.objects.create(poll=poll, **result_data)
        return poll """


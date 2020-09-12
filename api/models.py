import requests
import uuid
from django.db import models

class BaseAbgeordnetenwatchManager(models.Manager):
    def get_queryset(self):
        pass

# Create your models here.
class Politician(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    abgeordnetenwatch_id = models.IntegerField()
    wikidata_id = models.CharField(max_length=10)

    def get_abgeordnetenwatch_instance(self):
        if hasattr(self, 'abgeordnetenwatch_data'):
            pass
        else:
            r = requests.get(f'https://www.abgeordnetenwatch.de/api/v2/politicians/{self.abgeordnetenwatch_id}')
            self.abgeordnetenwatch_data = r.json()['data']

    @property
    def name(self):
        self.get_abgeordnetenwatch_instance()
        return self.abgeordnetenwatch_data['label']

    @property
    def occupation(self):
        self.get_abgeordnetenwatch_instance()
        return self.abgeordnetenwatch_data['occupation']

    @property
    def party(self):
        self.get_abgeordnetenwatch_instance()
        return self.abgeordnetenwatch_data['party']['label']

class Vote(models.Model):
    abgeordnetenwatch_id = models.IntegerField()
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)

    def get_abgeordnetenwatch_instance(self):
        if hasattr(self, 'abgeordnetenwatch_data'):
            pass
        else:
            r = requests.get(f'https://www.abgeordnetenwatch.de/api/v2/votes/{self.abgeordnetenwatch_id}')
            self.abgeordnetenwatch_data = r.json()['data']
            print("HALLO", self.abgeordnetenwatch_data)

    @property
    def poll(self):
        print('poll')
        self.get_abgeordnetenwatch_instance()
        return self.abgeordnetenwatch_data['poll']['id']

class PollResult(models.Model):
    yes = models.IntegerField(blank=True, null=True)
    no = models.IntegerField(blank=True, null=True)
    abstain = models.IntegerField(blank=True, null=True)
    no_show = models.IntegerField(blank=True, null=True)
    result = models.CharField(blank=True, null=True, max_length=12)

class Poll(models.Model):
    abgeordnetenwatch_id = models.IntegerField(null=True, blank=True)
    abgeordnetenwatch_url = models.URLField(null=True, blank=True)
    #yes = models.IntegerField(default=0)
    #no = models.IntegerField(default=0)
    #abstain = models.IntegerField(default=0)
    #no_show = models.IntegerField(default=0)
    title = models.CharField(max_length=256, blank=True, null=True)
    abstract = models.CharField(max_length=999, blank=True, null=True)
    yes = models.IntegerField(blank=True, null=True)
    no = models.IntegerField(blank=True, null=True)
    abstain = models.IntegerField(blank=True, null=True)
    no_show = models.IntegerField(blank=True, null=True)
    result = models.CharField(blank=True, null=True, max_length=12)

    def get_abgeordnetenwatch_instance(self):
        r = requests.get(f'https://www.abgeordnetenwatch.de/api/v2/votes?poll={self.abgeordnetenwatch_id}&range_end=999')
        self.votes = r.json()['data']
        self.abgeordnetenwatch_data = self.votes[0]['poll']

    

    """ @property
    def result(self):
        self.get_abgeordnetenwatch_instance()

        self.result = {
            'yes': 0,
            'no': 0,
            'abstain': 0,
            'no_show': 0,
        }


        for vote in self.votes:
            self.result[vote['vote']] += 1

        
        self.result['result'] = max(self.result, key=self.result.get) """

    """ def __init__(self, title, yes, no, abstain, no_show, total, result, abgeordnetenwatch_url):
        self.title = title
        self.yes = yes
        self.no = no
        self.abstain = abstain
        self.no_show = no_show
        self.total = total
        self.result = result
        self.abgeordnetenwatch_url = abgeordnetenwatch_url """

    #abgeordnetenwatch_id = models.IntegerField(blank=True, null=True)

    """ def get_abgeordnetenwatch_instance(self):
        if hasattr(self, 'abgeordnetenwatch_data'):
            pass
        else:
            r = requests.get(f'https://www.abgeordnetenwatch.de/api/v2/polls/{self.abgeordnetenwatch_id}')
            self.abgeordnetenwatch_data = r.json()['data']
            self.name = self.abgeordnetenwatch_data['label']
    
    @property
    def name(self):
        self.get_abgeordnetenwatch_instance()
        return self.abgeordnetenwatch_data['label'] """



class Controversy(models.Model):
    name = models.CharField(max_length=64)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)

class Article(models.Model):
    publisher = models.CharField(max_length=64)
    url = models.URLField()
    controversy = models.ForeignKey(Controversy, on_delete=models.CASCADE)
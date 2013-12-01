from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    SKILL_LEVELS = (
        ('advanced', 'advanced'),
        ('intermediate', 'intermediate'),
        ('beginner', 'beginner')
    )
    GENDERS = (
        ('male','male'),
        ('female','female')
    )
    STATES = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    )

    user           = models.OneToOneField(User, unique=True)
    age            = models.PositiveIntegerField(max_length=2)
    zipcode        = models.PositiveIntegerField(max_length=5)
    state          = models.CharField(max_length=2,choices=STATES)
    gender         = models.CharField(max_length=6,choices=GENDERS)
    one_k          = models.BooleanField(default=False)
    five_k         = models.BooleanField(default=False)
    ten_k          = models.BooleanField(default=False)
    one_mile       = models.BooleanField(default=False)
    five_mile      = models.BooleanField(default=False)
    ten_mile       = models.BooleanField(default=False)
    half_marathon  = models.BooleanField(default=False)
    full_marathon  = models.BooleanField(default=False)
    ultra_marathon = models.BooleanField(default=False)
    trail_run      = models.BooleanField(default=False)
    cross_country  = models.BooleanField(default=False)
    short_distance = models.BooleanField(default=False)
    long_distance  = models.BooleanField(default=False)
    competitive    = models.BooleanField(default=False)


    def __unicode__(self):
        return self.user.username

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from audiofield.fields import AudioField
from audiofield.models import AudioFile
#from django.contrib.auth.models import User
import os.path


# Create your models here.

# Add the audio field to your model


class MyAudioFile(models.Model):

    audio_file = AudioField(upload_to='api', blank=True,\
                        ext_whitelist=(".mp3", ".wav", ".ogg"),\
                        help_text=("Allowed type - .mp3, .wav, .ogg"))

    ivector = models.TextField(null=True)

    # Add this method to your model
    def audio_file_player(self):
        """audio player tag for admin"""
        print 'self.audio_file: ', self.audio_file
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = 'Audio file player'



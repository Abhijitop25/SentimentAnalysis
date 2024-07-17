from django import forms

class YouTubeForm(forms.Form):
    video_url = forms.URLField(label='YouTube Video URL')

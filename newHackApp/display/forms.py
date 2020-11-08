import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class patientDataInput(forms.Form):
    patientName = forms.CharField(label= 'Your Name', help_text="Enter a date between now and 4 weeks (default 3).", required= True)
    patientDescription = forms.CharField(label= 'Patient Description', help_text="Enter a date between now and 4 weeks (default 3).", required=True)
    patientAvailability = forms.DateField(label= 'Patient Availability', help_text="Enter a date between now and 4 weeks (default 3).", required=True)



    def clean_patientAvailability(self):

        #Calls Function on Patient  Availability input
        data = self.cleaned_data['patientAvailability']

        #Patient entered Availability that has passed current date
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Date passed'))

        #Patient entered Availability that is too far in the future
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_('Invalid date - 2+ weeks Ahead'))

        #Clean Return
        return data
    

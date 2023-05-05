from crispy_forms.layout import Layout,HTML
from django import forms
from tom_observations.facility import GenericObservationFacility, GenericObservationForm
from tom_targets.models import Target, TargetExtra
from swifttools.swift_too import TOO, Resolve
from django.core.management import call_command
from django.shortcuts import render  
from django.http import HttpResponse
from django.contrib.auth.models import User
   

class UVOTObservationForm(GenericObservationForm):

# Fields for user to fill in in Swift ToO form.
# Some fields are filled automatically by default for rapid submission of EM-GW candidates
    
    urgency = forms.IntegerField(required=False, label='ToO Urgency',initial=2)
    obs_type = forms.CharField(required=False, label='Observation type (Spectroscopy; Light curve; Position, Timing',initial='Light Curve')
    opt_mag = forms.FloatField(required=False, label='Optical Magnitude')
    opt_filt = forms.CharField(required=False, label='What filter was this measured in',initial='u')
    exposure = forms.FloatField(required=False, label='Exposure time requested [s]',initial=500)
    exp_time_just = forms.CharField(required=False, label='Time Justification', initial="500s to determine if source has faded")
    num_of_visits= forms.IntegerField(required=False, label='Number of visits [integer]',initial=1)
    monitoring_freq = forms.CharField(required=False, label='Frequency of visits')
    exp_time_per_visit = forms.FloatField(required=False, label='Exposure time per visit(s) [s]')
    uvot_mode = forms.CharField(required=False, label='UVOT filter mode (can write instructions or specific mode)', initial='0x01AB')
    science_just = forms.CharField(required=False, label='Science Justification', initial="500s to determine if source has faded")
    immediate_objective = forms.CharField(required=False, label='Immediate Objective',initial="To determine if source has faded.")
    source_type=forms.CharField(required=False, label='Source Type',initial='Optical/UV transient in GW error region')
    uvot_just = forms.CharField(required=False, label='UVOT Mode Justification', initial="Needs to be revised, do we want default as u or all filters?")
        
    def layout(self): 
        return Layout(
            'source_type',
            'urgency',
            'obs_type',
            'opt_mag',
            'opt_filt',
            'exposure',
            'num_of_visits',
            HTML('<p>If number of visits more than one change next exposure time per visit and monitoring frequency, otherwise leave blank.</p>'),
            'exp_time_per_visit',
            'monitoring_freq',
            'exp_time_just',
            'immediate_objective',
            'uvot_mode',
            'uvot_just',
            'science_just',
        )



class UVOTFacility(GenericObservationFacility):
    name = 'UVOT'
    observation_types = observation_forms = {
        'OBSERVATION': UVOTObservationForm
    }

    
    def data_products(self, observation_id, product_id=None):
       return []
   
    def get_form(self, observation_type):
        return UVOTObservationForm

    def get_observation_status(self, observation_id):
        return ['IN_PROGRESS']

    def get_observation_url(self, observation_id):
        return ''

    def get_observing_sites(self):
        return {}

    def get_terminal_observing_states(self):
        return ['IN_PROGRESS', 'COMPLETED']
    
    def submit_observation(self, observation_payload):

        # Send data from form to ToO submission tool in Swift API.
        # Additional fields here are filled in with defaul values to speed up submission for Swift EM-GW target follow-up
        too = TOO()
        too.debug = True   # Currently set to debug so won't actually submit ToO to Swift
        tid=(Target.objects.filter(pk=observation_payload['target_id']).values('id')[0]['id'])
        too.source_name=TargetExtra.objects.filter(target_id=tid,key='GWevent').values()[0]['value']+'_'+Target.objects.filter(pk=observation_payload['target_id']).values('name')[0]['name']
        too.ra=Target.objects.filter(pk=observation_payload['target_id']).values('ra')[0]['ra']
        too.dec=Target.objects.filter(pk=observation_payload['target_id']).values('dec')[0]['dec']
        too.username = observation_payload['too_username']
        too.shared_secret = observation_payload['too_secret']
        
        too.source_type='Optical/UV transient in GW error region'
        too.poserr=0.01

        too.source_type=observation_payload['params']['source_type']
        too.urgency=observation_payload['params']['urgency']
        too.obs_type=observation_payload['params']['obs_type']
        too.opt_mag=observation_payload['params']['opt_mag']
        too.opt_filt=observation_payload['params']['opt_filt']
        too.exposure=observation_payload['params']['exposure']
        too.exp_time_just=observation_payload['params']['exp_time_just']
        too.immediate_objective=observation_payload['params']['immediate_objective']
        too.science_just=observation_payload['params']['science_just']
        too.instrument='UVOT'
        too.uvot_mode=observation_payload['params']['uvot_mode']
        too.uvot_just=observation_payload['params']['uvot_just']

        print (too)
        #If want multiple visits need to add these lines (I haven't checked if this works yet)
        too.num_of_visits=observation_payload['params']['num_of_visits']
        if observation_payload['params']['num_of_visits'] >1:
            too.monitoring_freq=observation_payload['params']['monitoring_freq']
            too.exp_time_per_visit=observation_payload['params']['exp_time_per_visit']

        TargetExtra.objects.filter(target_id=tid,key='ToO?').update(bool_value=True)
        
        if too.validate():
            print("Good to go!")
        else:
            print(f"{too.status.status}. Errors: {too.status.errors}")
            
        #Need to add actual line to submit ToO, not done yet as testing.
            
        return [1]

    def validate_observation(self, observation_payload):
        return validate

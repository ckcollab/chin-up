# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Metric'
        db.create_table(u'chinup_metric', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description_worst', self.gf('django.db.models.fields.TextField')()),
            ('description_best', self.gf('django.db.models.fields.TextField')()),
            ('daily', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('monthly', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'chinup', ['Metric'])

        # Adding model 'MetricRecord'
        db.create_table(u'chinup_metricrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('measurement', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'chinup', ['MetricRecord'])


    def backwards(self, orm):
        # Deleting model 'Metric'
        db.delete_table(u'chinup_metric')

        # Deleting model 'MetricRecord'
        db.delete_table(u'chinup_metricrecord')


    models = {
        u'chinup.metric': {
            'Meta': {'object_name': 'Metric'},
            'daily': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description_best': ('django.db.models.fields.TextField', [], {}),
            'description_worst': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'chinup.metricrecord': {
            'Meta': {'object_name': 'MetricRecord'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['chinup']
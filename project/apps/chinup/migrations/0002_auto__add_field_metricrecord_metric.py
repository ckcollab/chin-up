# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MetricRecord.metric'
        db.add_column(u'chinup_metricrecord', 'metric',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['chinup.Metric']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MetricRecord.metric'
        db.delete_column(u'chinup_metricrecord', 'metric_id')


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
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chinup.Metric']"}),
            'notes': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['chinup']
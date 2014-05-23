# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Metric.description_worst'
        db.alter_column(u'chinup_metric', 'description_worst', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Metric.description_best'
        db.alter_column(u'chinup_metric', 'description_best', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'Metric.description_worst'
        db.alter_column(u'chinup_metric', 'description_worst', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Metric.description_best'
        db.alter_column(u'chinup_metric', 'description_best', self.gf('django.db.models.fields.TextField')(default=''))

    models = {
        u'chinup.metric': {
            'Meta': {'object_name': 'Metric'},
            'boolean': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'daily': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description_best': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_worst': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'chinup.metricrecord': {
            'Meta': {'object_name': 'MetricRecord'},
            'datetime': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.IntegerField', [], {'default': '5', 'blank': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chinup.Metric']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['chinup']
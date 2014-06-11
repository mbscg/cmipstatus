# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MemberConfig.compare_to'
        db.alter_column('expwatch_memberconfig', 'compare_to', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'MemberConfig.plot_area'
        db.alter_column('expwatch_memberconfig', 'plot_area', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):

        # Changing field 'MemberConfig.compare_to'
        db.alter_column('expwatch_memberconfig', 'compare_to', self.gf('django.db.models.fields.TextField')())

        # Changing field 'MemberConfig.plot_area'
        db.alter_column('expwatch_memberconfig', 'plot_area', self.gf('django.db.models.fields.TextField')())

    models = {
        'expwatch.alert': {
            'Meta': {'object_name': 'Alert'},
            'dismissed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expwatch.Exp']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'expwatch.exp': {
            'Meta': {'object_name': 'Exp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'expwatch.expmember': {
            'Meta': {'object_name': 'ExpMember'},
            'description': ('django.db.models.fields.TextField', [], {'default': "' '", 'max_length': '1024'}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expwatch.Exp']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restart_list': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1024'})
        },
        'expwatch.memberconfig': {
            'Meta': {'object_name': 'MemberConfig'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'compare_to': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {}),
            'last_gen': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expwatch.ExpMember']"}),
            'plot_area': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'variables': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['expwatch']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alert'
        db.create_table('expwatch_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expwatch.Exp'])),
            ('message', self.gf('django.db.models.fields.TextField')(default='')),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dismissed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('expwatch', ['Alert'])


    def backwards(self, orm):
        # Deleting model 'Alert'
        db.delete_table('expwatch_alert')


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
        }
    }

    complete_apps = ['expwatch']
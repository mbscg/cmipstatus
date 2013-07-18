# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Exp'
        db.create_table('expwatch_exp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('member', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('restart_list', self.gf('django.db.models.fields.CharField')(default='', max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=1024)),
        ))
        db.send_create_signal('expwatch', ['Exp'])


    def backwards(self, orm):
        # Deleting model 'Exp'
        db.delete_table('expwatch_exp')


    models = {
        'expwatch.exp': {
            'Meta': {'object_name': 'Exp'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'restart_list': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'})
        }
    }

    complete_apps = ['expwatch']
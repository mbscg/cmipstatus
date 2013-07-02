# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExpMember'
        db.create_table('expwatch_expmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expwatch.Exp'])),
            ('member', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('restart_list', self.gf('django.db.models.fields.CharField')(default='', max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=1024)),
        ))
        db.send_create_signal('expwatch', ['ExpMember'])

        # Deleting field 'Exp.restart_list'
        db.delete_column('expwatch_exp', 'restart_list')

        # Deleting field 'Exp.description'
        db.delete_column('expwatch_exp', 'description')

        # Deleting field 'Exp.member'
        db.delete_column('expwatch_exp', 'member')

        # Adding field 'Exp.members'
        db.add_column('expwatch_exp', 'members',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ExpMember'
        db.delete_table('expwatch_expmember')

        # Adding field 'Exp.restart_list'
        db.add_column('expwatch_exp', 'restart_list',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1024),
                      keep_default=False)

        # Adding field 'Exp.description'
        db.add_column('expwatch_exp', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=1024),
                      keep_default=False)

        # Adding field 'Exp.member'
        db.add_column('expwatch_exp', 'member',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Exp.members'
        db.delete_column('expwatch_exp', 'members')


    models = {
        'expwatch.exp': {
            'Meta': {'object_name': 'Exp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'expwatch.expmember': {
            'Meta': {'object_name': 'ExpMember'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024'}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expwatch.Exp']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restart_list': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'})
        }
    }

    complete_apps = ['expwatch']
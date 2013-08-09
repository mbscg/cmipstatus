# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Member'
        db.delete_table('cmipstatus_member')

        # Deleting model 'ConvReport'
        db.delete_table('cmipstatus_convreport')

        # Deleting model 'Comment'
        db.delete_table('cmipstatus_comment')

        # Deleting model 'ReportChangeLog'
        db.delete_table('cmipstatus_reportchangelog')

        # Deleting model 'MemberReport'
        db.delete_table('cmipstatus_memberreport')

        # Deleting model 'ExpReport'
        db.delete_table('cmipstatus_expreport')

        # Deleting model 'Experiment'
        db.delete_table('cmipstatus_experiment')


    def backwards(self, orm):
        # Adding model 'Member'
        db.create_table('cmipstatus_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Experiment'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('cmipstatus', ['Member'])

        # Adding model 'ConvReport'
        db.create_table('cmipstatus_convreport', (
            ('member', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cmipstatus', ['ConvReport'])

        # Adding model 'Comment'
        db.create_table('cmipstatus_comment', (
            ('text', self.gf('django.db.models.fields.TextField')(default='', max_length=2048)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Experiment'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
        ))
        db.send_create_signal('cmipstatus', ['Comment'])

        # Adding model 'ReportChangeLog'
        db.create_table('cmipstatus_reportchangelog', (
            ('message', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cmipstatus', ['ReportChangeLog'])

        # Adding model 'MemberReport'
        db.create_table('cmipstatus_memberreport', (
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Member'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cmipstatus', ['MemberReport'])

        # Adding model 'ExpReport'
        db.create_table('cmipstatus_expreport', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Experiment'])),
        ))
        db.send_create_signal('cmipstatus', ['ExpReport'])

        # Adding model 'Experiment'
        db.create_table('cmipstatus_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('cmipstatus', ['Experiment'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cmipstatus.people': {
            'Meta': {'object_name': 'People', '_ormbases': ['auth.User']},
            'about': ('django.db.models.fields.TextField', [], {'default': "'INPE GMAO Researcher'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'profile_default.png'", 'max_length': '1048'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cmipstatus']
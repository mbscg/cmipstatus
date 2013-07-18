# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'People'
        db.create_table('cmipstatus_people', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('about', self.gf('django.db.models.fields.TextField')(default='INPE GMAO Researcher')),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(default='profile_default.png', max_length=1048)),
        ))
        db.send_create_signal('cmipstatus', ['People'])

        # Adding model 'Experiment'
        db.create_table('cmipstatus_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('cmipstatus', ['Experiment'])

        # Adding model 'Member'
        db.create_table('cmipstatus_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Experiment'])),
        ))
        db.send_create_signal('cmipstatus', ['Member'])

        # Adding model 'Comment'
        db.create_table('cmipstatus_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Experiment'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('text', self.gf('django.db.models.fields.TextField')(default='', max_length=2048)),
        ))
        db.send_create_signal('cmipstatus', ['Comment'])

        # Adding model 'ExpReport'
        db.create_table('cmipstatus_expreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Experiment'])),
        ))
        db.send_create_signal('cmipstatus', ['ExpReport'])

        # Adding model 'MemberReport'
        db.create_table('cmipstatus_memberreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.Member'])),
        ))
        db.send_create_signal('cmipstatus', ['MemberReport'])

        # Adding model 'ConvReport'
        db.create_table('cmipstatus_convreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('member', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('cmipstatus', ['ConvReport'])

        # Adding model 'ReportChangeLog'
        db.create_table('cmipstatus_reportchangelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('cmipstatus', ['ReportChangeLog'])


    def backwards(self, orm):
        # Deleting model 'People'
        db.delete_table('cmipstatus_people')

        # Deleting model 'Experiment'
        db.delete_table('cmipstatus_experiment')

        # Deleting model 'Member'
        db.delete_table('cmipstatus_member')

        # Deleting model 'Comment'
        db.delete_table('cmipstatus_comment')

        # Deleting model 'ExpReport'
        db.delete_table('cmipstatus_expreport')

        # Deleting model 'MemberReport'
        db.delete_table('cmipstatus_memberreport')

        # Deleting model 'ConvReport'
        db.delete_table('cmipstatus_convreport')

        # Deleting model 'ReportChangeLog'
        db.delete_table('cmipstatus_reportchangelog')


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
        'cmipstatus.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '2048'})
        },
        'cmipstatus.convreport': {
            'Meta': {'object_name': 'ConvReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'cmipstatus.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'cmipstatus.expreport': {
            'Meta': {'object_name': 'ExpReport'},
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'cmipstatus.member': {
            'Meta': {'object_name': 'Member'},
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'cmipstatus.memberreport': {
            'Meta': {'object_name': 'MemberReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.Member']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'cmipstatus.people': {
            'Meta': {'object_name': 'People', '_ormbases': ['auth.User']},
            'about': ('django.db.models.fields.TextField', [], {'default': "'INPE GMAO Researcher'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'profile_default.png'", 'max_length': '1048'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'cmipstatus.reportchangelog': {
            'Meta': {'object_name': 'ReportChangeLog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
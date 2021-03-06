# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table('groupsite_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('long_content', self.gf('django.db.models.fields.TextField')(default=' ')),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('besm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('groupsite', ['News'])

        # Adding model 'NewsImg'
        db.create_table('groupsite_newsimg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsite.News'])),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('groupsite', ['NewsImg'])

        # Adding model 'NewsAttachment'
        db.create_table('groupsite_newsattachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsite.News'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('groupsite', ['NewsAttachment'])

        # Adding model 'ScienceThing'
        db.create_table('groupsite_sciencething', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('besm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('groupsite', ['ScienceThing'])

        # Adding model 'YoutubeVideo'
        db.create_table('groupsite_youtubevideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('science_thing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsite.ScienceThing'])),
            ('video_link', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('groupsite', ['YoutubeVideo'])

        # Adding model 'Graphic'
        db.create_table('groupsite_graphic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('science_thing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsite.ScienceThing'])),
            ('data_file', self.gf('django.db.models.fields.files.FileField')(max_length=102)),
        ))
        db.send_create_signal('groupsite', ['Graphic'])

        # Adding model 'Post'
        db.create_table('groupsite_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')(default=' ')),
            ('content', self.gf('django.db.models.fields.TextField')(default=' ')),
            ('using_markdown', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('besm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('groupsite', ['Post'])

        # Adding model 'PostImg'
        db.create_table('groupsite_postimg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsite.Post'])),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('groupsite', ['PostImg'])

        # Adding model 'PostAttachment'
        db.create_table('groupsite_postattachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsite.Post'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('groupsite', ['PostAttachment'])

        # Adding model 'Publication'
        db.create_table('groupsite_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=1024)),
            ('besm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('groupsite', ['Publication'])

        # Adding model 'NetworkInfo'
        db.create_table('groupsite_networkinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('lattes', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('linkedin', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('google_plus', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('github', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('bitbucket', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('groupsite', ['NetworkInfo'])

        # Adding model 'LattesCache'
        db.create_table('groupsite_lattescache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('last_update', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('groupsite', ['LattesCache'])

        # Adding model 'Editor'
        db.create_table('groupsite_editor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
        ))
        db.send_create_signal('groupsite', ['Editor'])

        # Adding model 'AmbarPeople'
        db.create_table('groupsite_ambarpeople', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
        ))
        db.send_create_signal('groupsite', ['AmbarPeople'])

        # Adding model 'AmbarReport'
        db.create_table('groupsite_ambarreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmipstatus.People'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=1024)),
        ))
        db.send_create_signal('groupsite', ['AmbarReport'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table('groupsite_news')

        # Deleting model 'NewsImg'
        db.delete_table('groupsite_newsimg')

        # Deleting model 'NewsAttachment'
        db.delete_table('groupsite_newsattachment')

        # Deleting model 'ScienceThing'
        db.delete_table('groupsite_sciencething')

        # Deleting model 'YoutubeVideo'
        db.delete_table('groupsite_youtubevideo')

        # Deleting model 'Graphic'
        db.delete_table('groupsite_graphic')

        # Deleting model 'Post'
        db.delete_table('groupsite_post')

        # Deleting model 'PostImg'
        db.delete_table('groupsite_postimg')

        # Deleting model 'PostAttachment'
        db.delete_table('groupsite_postattachment')

        # Deleting model 'Publication'
        db.delete_table('groupsite_publication')

        # Deleting model 'NetworkInfo'
        db.delete_table('groupsite_networkinfo')

        # Deleting model 'LattesCache'
        db.delete_table('groupsite_lattescache')

        # Deleting model 'Editor'
        db.delete_table('groupsite_editor')

        # Deleting model 'AmbarPeople'
        db.delete_table('groupsite_ambarpeople')

        # Deleting model 'AmbarReport'
        db.delete_table('groupsite_ambarreport')


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
        },
        'groupsite.ambarpeople': {
            'Meta': {'object_name': 'AmbarPeople'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'people': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"})
        },
        'groupsite.ambarreport': {
            'Meta': {'object_name': 'AmbarReport'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '1024'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'groupsite.editor': {
            'Meta': {'object_name': 'Editor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'people': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"})
        },
        'groupsite.graphic': {
            'Meta': {'object_name': 'Graphic'},
            'data_file': ('django.db.models.fields.files.FileField', [], {'max_length': '102'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'science_thing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsite.ScienceThing']"})
        },
        'groupsite.lattescache': {
            'Meta': {'object_name': 'LattesCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'people': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'groupsite.networkinfo': {
            'Meta': {'object_name': 'NetworkInfo'},
            'bitbucket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'github': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'google_plus': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattes': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'linkedin': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'people': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'groupsite.news': {
            'Meta': {'object_name': 'News'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'besm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_content': ('django.db.models.fields.TextField', [], {'default': "' '"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'groupsite.newsattachment': {
            'Meta': {'object_name': 'NewsAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '1024'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsite.News']"})
        },
        'groupsite.newsimg': {
            'Meta': {'object_name': 'NewsImg'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsite.News']"})
        },
        'groupsite.post': {
            'Meta': {'object_name': 'Post'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'besm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "' '"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "' '"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'using_markdown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'groupsite.postattachment': {
            'Meta': {'object_name': 'PostAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '1024'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsite.Post']"})
        },
        'groupsite.postimg': {
            'Meta': {'object_name': 'PostImg'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsite.Post']"})
        },
        'groupsite.publication': {
            'Meta': {'object_name': 'Publication'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmipstatus.People']"}),
            'besm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '1024'}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'groupsite.sciencething': {
            'Meta': {'object_name': 'ScienceThing'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'besm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'groupsite.youtubevideo': {
            'Meta': {'object_name': 'YoutubeVideo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'science_thing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsite.ScienceThing']"}),
            'video_link': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['groupsite']
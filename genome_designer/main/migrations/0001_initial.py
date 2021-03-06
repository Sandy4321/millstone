# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'main_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='ecf4eeb4', unique=True, max_length=8)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'main', ['UserProfile'])

        # Adding model 'Dataset'
        db.create_table(u'main_dataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='6b0704f0', unique=True, max_length=8)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('filesystem_location', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('filesystem_idx_location', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='READY', max_length=40)),
        ))
        db.send_create_signal(u'main', ['Dataset'])

        # Adding model 'Project'
        db.create_table(u'main_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='e5bb40ee', unique=True, max_length=8)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('s3_backed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['Project'])

        # Adding model 'Chromosome'
        db.create_table(u'main_chromosome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='b34f7c93', unique=True, max_length=8)),
            ('reference_genome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ReferenceGenome'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('num_bases', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'main', ['Chromosome'])

        # Adding model 'ReferenceGenome'
        db.create_table(u'main_referencegenome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='d1469408', unique=True, max_length=8)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Project'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('variant_key_map', self.gf('main.custom_fields.PostgresJsonField')()),
            ('is_materialized_variant_view_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['ReferenceGenome'])

        # Adding M2M table for field dataset_set on 'ReferenceGenome'
        m2m_table_name = db.shorten_name(u'main_referencegenome_dataset_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('referencegenome', models.ForeignKey(orm[u'main.referencegenome'], null=False)),
            ('dataset', models.ForeignKey(orm[u'main.dataset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['referencegenome_id', 'dataset_id'])

        # Adding model 'ExperimentSample'
        db.create_table(u'main_experimentsample', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='b8f40901', unique=True, max_length=8)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Project'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('data', self.gf('main.custom_fields.PostgresJsonField')()),
        ))
        db.send_create_signal(u'main', ['ExperimentSample'])

        # Adding M2M table for field dataset_set on 'ExperimentSample'
        m2m_table_name = db.shorten_name(u'main_experimentsample_dataset_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experimentsample', models.ForeignKey(orm[u'main.experimentsample'], null=False)),
            ('dataset', models.ForeignKey(orm[u'main.dataset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experimentsample_id', 'dataset_id'])

        # Adding model 'AlignmentGroup'
        db.create_table(u'main_alignmentgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='d9efcad4', unique=True, max_length=8)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('reference_genome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ReferenceGenome'])),
            ('aligner', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NOT_STARTED', max_length=40)),
        ))
        db.send_create_signal(u'main', ['AlignmentGroup'])

        # Adding M2M table for field dataset_set on 'AlignmentGroup'
        m2m_table_name = db.shorten_name(u'main_alignmentgroup_dataset_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alignmentgroup', models.ForeignKey(orm[u'main.alignmentgroup'], null=False)),
            ('dataset', models.ForeignKey(orm[u'main.dataset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['alignmentgroup_id', 'dataset_id'])

        # Adding model 'ExperimentSampleToAlignment'
        db.create_table(u'main_experimentsampletoalignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='4e021096', unique=True, max_length=8)),
            ('alignment_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.AlignmentGroup'])),
            ('experiment_sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ExperimentSample'])),
        ))
        db.send_create_signal(u'main', ['ExperimentSampleToAlignment'])

        # Adding M2M table for field dataset_set on 'ExperimentSampleToAlignment'
        m2m_table_name = db.shorten_name(u'main_experimentsampletoalignment_dataset_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experimentsampletoalignment', models.ForeignKey(orm[u'main.experimentsampletoalignment'], null=False)),
            ('dataset', models.ForeignKey(orm[u'main.dataset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experimentsampletoalignment_id', 'dataset_id'])

        # Adding model 'Variant'
        db.create_table(u'main_variant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='2d7d8c65', unique=True, max_length=8)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('reference_genome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ReferenceGenome'])),
            ('chromosome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Chromosome'])),
            ('position', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ref_value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Variant'])

        # Adding model 'VariantCallerCommonData'
        db.create_table(u'main_variantcallercommondata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Variant'])),
            ('source_dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Dataset'])),
            ('data', self.gf('main.custom_fields.PostgresJsonField')()),
            ('alignment_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.AlignmentGroup'])),
        ))
        db.send_create_signal(u'main', ['VariantCallerCommonData'])

        # Adding model 'VariantAlternate'
        db.create_table(u'main_variantalternate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='43363c41', unique=True, max_length=8)),
            ('variant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Variant'], null=True)),
            ('alt_value', self.gf('django.db.models.fields.TextField')()),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data', self.gf('main.custom_fields.PostgresJsonField')()),
        ))
        db.send_create_signal(u'main', ['VariantAlternate'])

        # Adding model 'VariantEvidence'
        db.create_table(u'main_variantevidence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='c511c486', unique=True, max_length=8)),
            ('experiment_sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ExperimentSample'])),
            ('variant_caller_common_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.VariantCallerCommonData'])),
            ('data', self.gf('main.custom_fields.PostgresJsonField')()),
        ))
        db.send_create_signal(u'main', ['VariantEvidence'])

        # Adding M2M table for field variantalternate_set on 'VariantEvidence'
        m2m_table_name = db.shorten_name(u'main_variantevidence_variantalternate_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('variantevidence', models.ForeignKey(orm[u'main.variantevidence'], null=False)),
            ('variantalternate', models.ForeignKey(orm[u'main.variantalternate'], null=False))
        ))
        db.create_unique(m2m_table_name, ['variantevidence_id', 'variantalternate_id'])

        # Adding model 'VariantToVariantSet'
        db.create_table(u'main_varianttovariantset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Variant'])),
            ('variant_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.VariantSet'])),
        ))
        db.send_create_signal(u'main', ['VariantToVariantSet'])

        # Adding M2M table for field sample_variant_set_association on 'VariantToVariantSet'
        m2m_table_name = db.shorten_name(u'main_varianttovariantset_sample_variant_set_association')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('varianttovariantset', models.ForeignKey(orm[u'main.varianttovariantset'], null=False)),
            ('experimentsample', models.ForeignKey(orm[u'main.experimentsample'], null=False))
        ))
        db.create_unique(m2m_table_name, ['varianttovariantset_id', 'experimentsample_id'])

        # Adding model 'VariantSet'
        db.create_table(u'main_variantset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='4d8415ac', unique=True, max_length=8)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('reference_genome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ReferenceGenome'])),
        ))
        db.send_create_signal(u'main', ['VariantSet'])

        # Adding M2M table for field dataset_set on 'VariantSet'
        m2m_table_name = db.shorten_name(u'main_variantset_dataset_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('variantset', models.ForeignKey(orm[u'main.variantset'], null=False)),
            ('dataset', models.ForeignKey(orm[u'main.dataset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['variantset_id', 'dataset_id'])

        # Adding model 'Region'
        db.create_table(u'main_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(default='14e51a55', unique=True, max_length=8)),
            ('reference_genome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ReferenceGenome'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'main', ['Region'])

        # Adding model 'RegionInterval'
        db.create_table(u'main_regioninterval', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Region'])),
            ('start', self.gf('django.db.models.fields.BigIntegerField')()),
            ('end', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'main', ['RegionInterval'])

        # Adding model 'S3File'
        db.create_table(u'main_s3file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bucket', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['S3File'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'main_userprofile')

        # Deleting model 'Dataset'
        db.delete_table(u'main_dataset')

        # Deleting model 'Project'
        db.delete_table(u'main_project')

        # Deleting model 'Chromosome'
        db.delete_table(u'main_chromosome')

        # Deleting model 'ReferenceGenome'
        db.delete_table(u'main_referencegenome')

        # Removing M2M table for field dataset_set on 'ReferenceGenome'
        db.delete_table(db.shorten_name(u'main_referencegenome_dataset_set'))

        # Deleting model 'ExperimentSample'
        db.delete_table(u'main_experimentsample')

        # Removing M2M table for field dataset_set on 'ExperimentSample'
        db.delete_table(db.shorten_name(u'main_experimentsample_dataset_set'))

        # Deleting model 'AlignmentGroup'
        db.delete_table(u'main_alignmentgroup')

        # Removing M2M table for field dataset_set on 'AlignmentGroup'
        db.delete_table(db.shorten_name(u'main_alignmentgroup_dataset_set'))

        # Deleting model 'ExperimentSampleToAlignment'
        db.delete_table(u'main_experimentsampletoalignment')

        # Removing M2M table for field dataset_set on 'ExperimentSampleToAlignment'
        db.delete_table(db.shorten_name(u'main_experimentsampletoalignment_dataset_set'))

        # Deleting model 'Variant'
        db.delete_table(u'main_variant')

        # Deleting model 'VariantCallerCommonData'
        db.delete_table(u'main_variantcallercommondata')

        # Deleting model 'VariantAlternate'
        db.delete_table(u'main_variantalternate')

        # Deleting model 'VariantEvidence'
        db.delete_table(u'main_variantevidence')

        # Removing M2M table for field variantalternate_set on 'VariantEvidence'
        db.delete_table(db.shorten_name(u'main_variantevidence_variantalternate_set'))

        # Deleting model 'VariantToVariantSet'
        db.delete_table(u'main_varianttovariantset')

        # Removing M2M table for field sample_variant_set_association on 'VariantToVariantSet'
        db.delete_table(db.shorten_name(u'main_varianttovariantset_sample_variant_set_association'))

        # Deleting model 'VariantSet'
        db.delete_table(u'main_variantset')

        # Removing M2M table for field dataset_set on 'VariantSet'
        db.delete_table(db.shorten_name(u'main_variantset_dataset_set'))

        # Deleting model 'Region'
        db.delete_table(u'main_region')

        # Deleting model 'RegionInterval'
        db.delete_table(u'main_regioninterval')

        # Deleting model 'S3File'
        db.delete_table(u'main_s3file')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.alignmentgroup': {
            'Meta': {'object_name': 'AlignmentGroup'},
            'aligner': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dataset_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Dataset']", 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'reference_genome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ReferenceGenome']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NOT_STARTED'", 'max_length': '40'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'f26b44e3'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.chromosome': {
            'Meta': {'object_name': 'Chromosome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'num_bases': ('django.db.models.fields.BigIntegerField', [], {}),
            'reference_genome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ReferenceGenome']"}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'b31bd7eb'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'filesystem_idx_location': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'filesystem_location': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'READY'", 'max_length': '40'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'59c290f7'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.experimentsample': {
            'Meta': {'object_name': 'ExperimentSample'},
            'data': ('main.custom_fields.PostgresJsonField', [], {}),
            'dataset_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Dataset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Project']"}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'b7158953'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.experimentsampletoalignment': {
            'Meta': {'object_name': 'ExperimentSampleToAlignment'},
            'alignment_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.AlignmentGroup']"}),
            'dataset_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Dataset']", 'null': 'True', 'blank': 'True'}),
            'experiment_sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ExperimentSample']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'d86b9261'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.UserProfile']"}),
            's3_backed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'3774f5e3'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.referencegenome': {
            'Meta': {'object_name': 'ReferenceGenome'},
            'dataset_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Dataset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_materialized_variant_view_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Project']"}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'5b16878e'", 'unique': 'True', 'max_length': '8'}),
            'variant_key_map': ('main.custom_fields.PostgresJsonField', [], {})
        },
        u'main.region': {
            'Meta': {'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'reference_genome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ReferenceGenome']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'0faedb91'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.regioninterval': {
            'Meta': {'object_name': 'RegionInterval'},
            'end': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Region']"}),
            'start': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'main.s3file': {
            'Meta': {'object_name': 'S3File'},
            'bucket': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'dba1d6b5'", 'unique': 'True', 'max_length': '8'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'main.variant': {
            'Meta': {'object_name': 'Variant'},
            'chromosome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Chromosome']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.BigIntegerField', [], {}),
            'ref_value': ('django.db.models.fields.TextField', [], {}),
            'reference_genome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ReferenceGenome']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'60015181'", 'unique': 'True', 'max_length': '8'})
        },
        u'main.variantalternate': {
            'Meta': {'object_name': 'VariantAlternate'},
            'alt_value': ('django.db.models.fields.TextField', [], {}),
            'data': ('main.custom_fields.PostgresJsonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'7c377953'", 'unique': 'True', 'max_length': '8'}),
            'variant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Variant']", 'null': 'True'})
        },
        u'main.variantcallercommondata': {
            'Meta': {'object_name': 'VariantCallerCommonData'},
            'alignment_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.AlignmentGroup']"}),
            'data': ('main.custom_fields.PostgresJsonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Dataset']"}),
            'variant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Variant']"})
        },
        u'main.variantevidence': {
            'Meta': {'object_name': 'VariantEvidence'},
            'data': ('main.custom_fields.PostgresJsonField', [], {}),
            'experiment_sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ExperimentSample']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'8bc3474f'", 'unique': 'True', 'max_length': '8'}),
            'variant_caller_common_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.VariantCallerCommonData']"}),
            'variantalternate_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.VariantAlternate']", 'symmetrical': 'False'})
        },
        u'main.variantset': {
            'Meta': {'object_name': 'VariantSet'},
            'dataset_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Dataset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'reference_genome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ReferenceGenome']"}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'b9d3b0bf'", 'unique': 'True', 'max_length': '8'}),
            'variants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Variant']", 'null': 'True', 'through': u"orm['main.VariantToVariantSet']", 'blank': 'True'})
        },
        u'main.varianttovariantset': {
            'Meta': {'object_name': 'VariantToVariantSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample_variant_set_association': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.ExperimentSample']", 'null': 'True', 'blank': 'True'}),
            'variant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Variant']"}),
            'variant_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.VariantSet']"})
        }
    }

    complete_apps = ['main']
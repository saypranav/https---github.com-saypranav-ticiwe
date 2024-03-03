from django.db import models
# from django.contrib.gis.db import models as geo_model
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.utils import timezone

# class Location(geo_model.Model):
#     name = models.CharField(max_length=100)
#     coordinates = models.PointField() # to store geographic coordinates

# class Area(geo_model.Model):
#     name = models.CharField(max_length=100)
#     boundary = models.PolygonField() # to store geographic boundaries

# class Route(geo_model.Model):
#     name = models.CharField(max_length=100)
#     path = models.LineStringField() # to store geographic paths/routes

class geo_locations(models.Model):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    foglio = models.TextField(blank=True, null=True)
    particella = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)
 
    class Meta:
        managed = True
        db_table = 'geo_locations'

class task_types(models.Model):
    type = models.TextField(blank=False, null=False, default="Undefined")
    description = models.TextField(blank=True, null=True)
    is_disabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'task_types'

class tasks(models.Model):
    type = models.ForeignKey(task_types, on_delete= models.DO_NOTHING, blank=True, null=True,db_index= True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    is_enabled = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'tasks'

# if required
# class calendar(models.Model):
#     task_id = models.ForeignKey(tasks, on_delete= models.DO_NOTHING, blank=True, null=True,db_index= True) 
#     added_date = models.DateTimeField(blank=True, null=True, default=None)
#     created_on = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'calendar'

class note_types(models.Model):
    type = models.TextField(blank=False, null=False, default="Undefined")
    description = models.TextField(blank=True, null=True)
    is_disabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'note_types'

class notes(models.Model):
    type = models.ForeignKey(task_types, on_delete= models.DO_NOTHING, blank=True, null=True,db_index= True)
    notes = models.TextField(blank=True, null=True)
    created_by_user_id = models.ForeignKey(User,on_delete= models.DO_NOTHING, blank=True, null=True) 
    added_date = models.DateTimeField(blank=True, null=True, default=None)
    is_enabled = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'notes'

class file_types(models.Model):
    type = models.TextField(blank=False, null=False, default="Undefined")
    description = models.TextField(blank=True, null=True)
    is_enabled = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'file_types'

class files(models.Model):
    type = models.ForeignKey(task_types, on_delete= models.DO_NOTHING, blank=True, null=True,db_index= True)
    file_id = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    created_by_user_id = models.ForeignKey(User,on_delete= models.DO_NOTHING, blank=True, null=True) 
    added_date = models.DateTimeField(blank=True, null=True, default=None)
    is_enabled = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'files'

@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user_id = models.TextField(verbose_name="user id", default='ABMS')
    emp_id = models.CharField(verbose_name="employee id", max_length=10, default='EmpID')
    dept_name = models.TextField(verbose_name="department name", default='ABMS')
    user_status = models.TextField(verbose_name="user status", default='New')
    user_description = models.TextField(verbose_name="user desciption", default='New user')
    otp = models.IntegerField(verbose_name="otp", default='1234')
    login_attempt = models.IntegerField(verbose_name="login_attempt", default=0)
    role_id = models.IntegerField(verbose_name="role id", default=5)
    is_validated = models.BooleanField(verbose_name="is validated", default=False)
    random_url = models.TextField(verbose_name="random url", default='default')
    otp_sent_time = models.DateTimeField(verbose_name="otp_sent_time", default='2021-01-01 11:21:05')
    url_valid_time = models.DateTimeField(verbose_name="url_valid_time", default='2021-01-01 11:21:05')
    is_first_time_user = models.BooleanField(db_column='IsFirstTimeUser', blank=True, null=True, default=True)
    created_on = models.DateTimeField(db_column='CreatedOn',default=timezone.now)
    modified_on = models.DateTimeField(db_column='ModifiedOn',default=timezone.now)
    offset_time = models.IntegerField(blank=True, null=True)
    is_workflow_engine_created = models.BooleanField(db_column='IsWorkflowEngineCreated', blank=True, null=True, default=False)
    is_pyramid_user_created = models.BooleanField(db_column='IsPyramidUserCreated', blank=True, null=True, default=False)
    workflow_default_service_user_created = models.BooleanField(db_column='workflow_default_service_user_created', blank=True, null=True, default=False)


class module_group(models.Model):
    module_group_id = models.AutoField(db_column='module_group_id',primary_key=True, db_index= True)
    module_group_name = models.TextField(db_column='module_group_name', blank=True, null=True,db_index= True)
    module_description = models.TextField(db_column='module_description', blank=True, null=True,db_index= True)
    is_role_created = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'module_group'

class resources_type(models.Model):
    resource_type_id = models.AutoField(db_column='resources_type_id',primary_key=True, db_index= True)
    resource_type_name = models.TextField(db_column='resources_type_name', blank=True, null=True,db_index= True) 
    table_name = models.TextField(db_column='table_name', blank=True, null=True,db_index= True) 
    class Meta:
        managed = True
        db_table = 'resources_type'

class modules(models.Model):
    module_id = models.AutoField(db_column='module_id',primary_key=True, db_index= True)
    module_name = models.TextField(db_column='module_name', blank=True, null=True,db_index= True) 
    module_tag = models.IntegerField(db_column='module_tag', blank=True, null=True,db_index= True)
    is_role_created = models.BooleanField(default=False)
    parent_tag = models.IntegerField(db_column='parent_tag', blank=True, null=True,db_index= True)
    
    class Meta:
        managed = True
        db_table = 'modules'

class module_group_map(models.Model):
    map_id = models.AutoField(db_column='map_id',primary_key=True, db_index= True)
    module_group_id = models.ForeignKey(module_group,db_column='module_group_id',on_delete= models.CASCADE, null= True, blank = True )
    module_id = models.ForeignKey(modules,db_column='module_id',on_delete= models.CASCADE,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'module_group_map'

class access_control(models.Model):
    access_id = models.AutoField(db_column='access_id',primary_key=True, db_index= True)
    access_name = models.TextField(db_column='access_name',null= True, blank = True )
    access_description = models.TextField(db_column='access_description',null= True, blank = True )
    class Meta:
        managed = True
        db_table = 'access_control'
        
class authorization_roles(models.Model):
    role_id = models.AutoField(db_column='role_id', primary_key=True)
    role_name = models.TextField(db_column='role_name', blank=True, null=True)
    roles_decription = models.TextField(db_column='roles_decription', blank=True, null=True)
    #rpa_ID = models.IntegerField(db_column='RpaID', blank=True, null=True)
    resources_type = models.ForeignKey(resources_type, db_column='resources_type', on_delete=models.CASCADE)
    resource_id = models.IntegerField(db_column='resource_id')
    access_id = models.ForeignKey(access_control, db_column='access_id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(db_column='created_on',default=timezone.now)
    modified_on = models.DateTimeField(db_column='modified_on',default=timezone.now)
    

    class Meta:
        managed = True
        db_table = 'authorization_roles'

class user_roles_map(models.Model):
    map_id = models.AutoField(db_column='map_id',primary_key=True, db_index= True)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE, default = 1)
    user_role = models.ForeignKey(authorization_roles, db_column='user_role', on_delete=models.CASCADE, default = 1)
    class Meta:
        managed = True
        db_table = 'user_roles_map'

class user_group_details(models.Model):
    user = models.OneToOneField(Group, on_delete=models.CASCADE)
    user_group_description = models.TextField(blank=True, null=True)

class user_group(models.Model):
    user_group_id = models.AutoField(primary_key=True, db_index= True)
    user_group_name = models.TextField(db_index= True)
    user_group_description = models.TextField(blank=True, null=True,db_index= True)
    class Meta:
        managed = True
        db_table = 'user_group'

class user_group_map(models.Model):
    user_group_map_id = models.AutoField(primary_key=True, db_index= True)
    # user_group_id = models.ForeignKey(Group, db_column='user_group_id', on_delete=models.CASCADE)
    user_group_id = models.ForeignKey(user_group, db_column='user_group_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'user_group_map'

class user_group_role_map(models.Model):
    map_id = models.AutoField(primary_key=True, db_index= True)
    # user_group_id = models.ForeignKey(Group, db_column='user_group_id', on_delete=models.CASCADE)
    user_group_id = models.ForeignKey(user_group, db_column='user_group_id', on_delete=models.CASCADE)
    user_group_role_id = models.ForeignKey(authorization_roles, db_column='user_group_role_id', on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'user_group_role_map'

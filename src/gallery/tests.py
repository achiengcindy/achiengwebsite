from django.test import TestCase

# Create your tests here.

# Django dumpdata and loaddata# dumpdata command

-   It is a django management command, which can be use to backup(export) you model instances or whole database

# dumpdata for basic database dump

-   Following command will dump whole database in to a  `db.json`  file

```
./manage.py dumpdata > db.json
```

# dumpdata for backup specific app

-   Following command will dump the content in django  `admin`  app into  `admin.json`  file

```
./manage.py dumpdata admin > admin.json
```

# dumpdata for backup specific table

-   Following command will dump only the content in django  `admin.logentry`  table

```
./manage.py dumpdata admin.logentry > logentry.json
```

-   Following command will dump the content in django  `auth.user`  table

```
./manage.py dumpdata auth.user > user.json
```

# dumpdata (--exclude)

-   You can use  `--exclude`  option to specify apps/tables which don't need being dumped
    
-   Following command will dump the whole database with out including  `auth.permission`  table content
    

```
./manage.py dumpdata --exclude auth.permission > db.json
```

# dumpdata (--indent)

-   By default,  `dumpdata`  will output all data on a single line. It isn’t easy for humans to read
    
-   You can use the  `--indent`  option to pretty-print the output with a number of indentation spaces
    

```
./manage.py dumpdata auth.user --indent 2 > user.json
`
# dumpdata (--format)

-   By default, dumpdata will format its output in JSON
    
-   You can specify the format using --format option
    
-   Command supports for following formats(serialization formats)
    

1.  json
2.  xml
3.  yaml

```
./manage.py dumpdata auth.user --indent 2 --format xml > user.xml

# loaddata command

-   This command can be use to load the fixtures(database dumps) into database

```
./manage.py loaddata user.json
```

-   This command will add the  `user.json`  file content into the database

# Restore fresh database

-   When you backup whole database by using  `dumpdata`  command, it will backup all the database tables
    
-   If you use this database dump to load the fresh database(in another django project), it can be causes  `IntegrityError`  (If you  `loaddata`  in same database it works fine)
    
-   To fix this problem, make sure to backup the database by excluding  `contenttypes`  and  `auth.permissions`  tables
    

```
./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```

-   Now you can use  `loaddata`  command with a fresh database

```
./manage.py loaddata db.json











  MochaHost   
Search ( / )
  
 Setup Python App
Operations to perform:
Apply all migrations: accounts, admin, auth, blog, contenttypes, flatpages, newsletter, sessions, sites, taggit, thumbnail
Running migrations:
Applying blog.0002_auto_20190303_1715...Traceback (most recent call last):
File "/home/pristol/public_html/src/manage.py", line 15, in <module>
execute_from_command_line(sys.argv)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
utility.execute()
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/core/management/__init__.py", line 375, in execute
self.fetch_command(subcommand).run_from_argv(self.argv)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/core/management/base.py", line 316, in run_from_argv
self.execute(*args, **cmd_options)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/core/management/base.py", line 353, in execute
output = self.handle(*args, **options)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/core/management/base.py", line 83, in wrapped
res = handle_func(*args, **kwargs)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/core/management/commands/migrate.py", line 203, in handle
fake_initial=fake_initial,
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/db/migrations/executor.py", line 117, in migrate
state = self._migrate_all_forwards(state, plan, full_plan, fake=fake, fake_initial=fake_initial)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/db/migrations/executor.py", line 147, in _migrate_all_forwards
state = self.apply_migration(state, migration, fake=fake, fake_initial=fake_initial)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/db/migrations/executor.py", line 244, in apply_migration
state = migration.apply(state, schema_editor)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/db/migrations/migration.py", line 114, in apply
operation.state_forwards(self.app_label, project_state)
File "/home/pristol/virtualenv/public__html_src/3.6/lib/python3.6/site-packages/django/db/migrations/operations/fields.py", line 144, in state_forwards
delay = not old_field.is_relation
AttributeError: 'NoneType' object has no attribute 'is_relation'
Setup new application
Python version	
App Directory /home/pristol/	
App Domain/URI	
Existing applications (2)
App Directory	public_html/src	Edit
App URI	achiengcindy.com/	Edit
WSGI file location		Edit
Python version		 
modules	
show
 
Execute command	
python /home/pristol/public_html/src/manage.py migrate
 
Command for entering to virtual environment	source /home/pristol/virtualenv/public__html_src/3.6/bin/activate	 
App Directory	decor.co.ke/src	Edit
App URI	decor.achiengcindy.com/	Edit
Additional domains	
decor.co.ke/
WSGI file location		Edit
Python version		 
modules	
show
 
Execute command	
0-9a-zA-Z /_-.,"~>< symbols are allowed
 
Command for entering to virtual environment	source /home/pristol/virtualenv/decor.co.ke_src/3.6/bin/activate	 
 Go Back
Home
Trademarks
Documentation
Help
  cPanel, Inc.  70.0.66
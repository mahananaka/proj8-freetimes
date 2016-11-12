#
#  Project 7: Pull Google calendar events 


# ###########################################
# Configuration options
#     Makefile.local is produced by the 'configure' script
#     client_secrets.py must be placed in the secrets directory
#
Makefile.local: 
	echo "You must run the 'configure' script before using make"

include Makefile.local


#  Compile web-site assets (things that will be in the 'static' 
#  directory)
#
#  Largely this means concatenating and 'minifying' some javascript and css 
#  assets to reduce browser load time (fewer http requests). 
#

# A locally installed copy of browserify
BROWSERIFY=static/js/node_modules/browserify/bin/cmd.js

#
#  The files we generate at build-time
# 
DERIVED = static/js/*.min.js static/js/node_modules

##############
#  Virtual environment

env:
	$(PYVENV)  env
	($(INVENV) pip install -r requirements.txt )

# Many recipes need to be run in the virtual environment, 
# so run them as $(INVENV) command
INVENV = . env/bin/activate ;

#  Note on javascript source files: 
#  Although nodejs is installed in Raspbian, 
#  npm is not.  (Just like pyvenv not being installed 
#  with Python3 ... what were they thinking?) 
#  We'll get by without npm and browserify. 
# 

# 'make run' runs Flask's built-in test server, 
#  with debugging turned on unless it is unset in CONFIG.py
# 
run:	env
	($(INVENV) python3 flask_main.py) ||  true

# 'make service' runs as a background job under the gunicorn 
#  WSGI server. FIXME:  A real production service would use 
#  NGINX in combination with gunicorn to prevent DOS attacks. 
#
#  For now we are running gunicorn on its default port of 8000. 
#  FIXME: Configuration builder could put the desired port number
#  into Makefile.local. 
# 
service:	env
	echo "Launching green unicorn in background"
	($(INVENV) gunicorn --bind="0.0.0.0:8000" flask_main:app )&

##
## Run test suite. 
## Currently 'nose' takes care of this, but in future we 
## might add test cases that can't be run under 'nose' 
##
test:	env
	$(INVENV) nosetests -s

##
## Preserve virtual environment for git repository
## to duplicate it on other targets
##
dist:	env
	$(INVENV) pip freeze >requirements.txt


# 'clean' and 'veryclean' are typically used before checking 
# things into git.  'clean' should leave the project ready to 
# run, while 'veryclean' may leave project in a state that 
# requires re-running installation and configuration steps
# 
clean:
	rm -f *.pyc
	rm -rf __pycache__

veryclean:
	make clean
	rm -f CONFIG.py
	rm -rf env
	rm -f Makefile.local



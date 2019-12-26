# DjangoBlogApp
 
# Requirements
Python 3.6 & up
Virtual Environment (pipenv or virtualenv)

# 1. Create Virtual Environment & Install Django
<code>
cd /path/to/dev/folder
mkdir try_django
cd try_django
pipenv --python 3.6 install django==2.2
pipenv shell
</code>

# 2. Create Django Project
<code>
cd /path/to/dev/folder
mkdir src
cd src
django-admin startproject try_django .
</code>

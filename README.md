#learning_azure
## Development
### Pre-requisites
- PostgreSQL
- Python3.6
- Virtualenv

### Install & Configure PostgreSQL - Please use Azure ressource "w1duw" 
Please refer to this [link](https://www.postgresql.org/download/) to install PostgreSQL.

Configure PostgreSQL:
```
sudo su postgres
psql
CREATE DATABASE db_name;
CREATE USER my_username WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE "db_name to my_username;
```

### Clone and Install Project
```
git clone git@github.com:jaystary/learning_azure.git
cd learning_azure
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Environment Variables in KeyVault
```
We store all environment variables in Azure KeyVault and reference them in code (see dev.py)
KeyVault Ressource: learning2

export AZURE_CLIENT_ID="2bf7f0fd-d2b4-4b34-83fd-59268adf07a9"

export AZURE_CLIENT_SECRET="Request it from jay"

export AZURE_TENANT_ID="78b03b78-f223-44e6-aa1d-7af413d79685"

Install the relevant packages for Azure from requirements.txt
If everything is set up correctly credential = DefaultAzureCredential() accesses the required credentials

```

Run
```
export DJANGO_SETTINGS_MODULE=config.settings.local
or 
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py migrate
python manage.py runserver
```

### Test
Go to following url on browser to test running of this project
http://127.0.0.1:8000/admin

Then go to following url to see swagger-doc for api endpoints.
http://127.0.0.1:8000/api/doc

### Sentry Logging
Documentation: https://docs.sentry.io/platforms/python/#integrating-the-sdk
Configured DSN through KeyVault https://9e7e239c5f4841cfaa2416fbffed41ef@sentry.io/1808837
Has to be configured in detail and integrated

Sentry captures all non-treated errors in middleware style
To capture individual events:
```
from sentry_sdk import capture_exception
from django.conf import settings

except Exception as e:
    capture_exception(e)

```
### Misc Considerations
Azure Postgres requires to have an IP in the firewall configured, otherwise the application will not run!


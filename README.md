#learning_azure
## Development
### Pre-requisites
- PostgreSQL
- Python3.6
- Virtualenv

### Install & Configure PostgreSQL - Please use Azure ressource "w1duw" 
Please refer to this [link](https://www.postgresql.org/download/) to install PostgreSQL.

The project is configured for a remote postgres instance that utilizes Azure Key Vault to load the data from
For local setup, follow the following steps and reconfigure the connection string:
```
sudo su postgres
psql
CREATE DATABASE db_name;
CREATE USER my_username WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE "db_name to my_username;
```

### Clone and Install Project
```
git clone git@github.com:gremloon/learning_azure.git
cd learning_azure
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Environment Variables in KeyVault
```
We store all environment variables in Azure KeyVault and reference them in code (see dev.py)
KeyVault Ressource: learning2

Install the relevant packages for Azure from requirements.txt
If everything is set up correctly  
credential = DefaultAzureCredential()  
accesses the required credentials

You might also have to run this command:
az keyvault set-policy --name learning2 --spn $AZURE_CLIENT_ID --secret-permissions backup delete get list

Pointer? After i was logged in locally on Azure CLI in the wrong Azure account it wouldnt allow me to log in, keep this in minds

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

Then go to following url to see signin based on azure AD B2C.
http://127.0.0.1:8000/azure_auth/login

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


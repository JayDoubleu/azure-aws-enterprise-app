# azure-aws-enterprise-app

> **⚠️ ARCHIVED**: This repository was created when there was no automation available to create AWS Enterprise Apps on Azure for AWS SSO authentication. This functionality is now available through various methods and tools like Terraform, making this repository obsolete.

Creates AWS Enterprise app on Azure

Requirements: 
- azure-cli (pip install azure-cli)
- az command in $PATH
- logged in to azure (az login)

````
usage: create.py [-h] [--appname APPNAME] [--appdesc APPDESC] [--email EMAIL]
                 [--accountid ACCOUNTID] [--accesskey ACCESSKEY]
                 [--secretkey SECRETKEY]

Creates AWS Enterprise app on Azure

optional arguments:
  -h, --help            show this help message and exit
  --appname APPNAME     Application name
  --appdesc APPDESC     Application description
  --email EMAIL         SAML Signing Certificate Notification Email
  --accountid ACCOUNTID
                        AWS Account ID
  --accesskey ACCESSKEY
                        AWS Access Key ID
  --secretkey SECRETKEY
                        AWS Secret Access Key
````

import time
import json
import uuid
import argparse
import requests
import subprocess

parser = argparse.ArgumentParser(
    description='Creates AWS Enterprise app on Azure')
parser.add_argument(
    '--appname', type=str, help='Application name', required=False, default="")
parser.add_argument(
    '--appdesc',
    type=str,
    help='Application description',
    required=False,
    default="")
parser.add_argument(
    '--email',
    type=str,
    help='SAML Signing Certificate Notification Email',
    required=False,
    default="")
parser.add_argument(
    '--accountid', type=str, help='AWS Account ID', required=False, default="")
parser.add_argument(
    '--accesskey',
    type=str,
    help='AWS Access Key ID',
    required=False,
    default="")
parser.add_argument(
    '--secretkey',
    type=str,
    help='AWS Secret Access Key',
    required=False,
    default="")
args = parser.parse_args()

email = args.email
app_name = args.appname
app_description = args.appdesc
account_id = args.accountid
aws_access_key_id = args.accesskey
aws_secret_access_key = args.secretkey

idp_identifier = "https://signin.aws.amazon.com/saml#%s" % account_id
api_url = "https://main.iam.ad.ext.azure.com/api"
access_token = json.loads(
    subprocess.check_output([
        "az", "account", "get-access-token", "--resource",
        "74658136-14ec-4630-ad9b-26e160ff0fc6"
    ]))['accessToken']

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + access_token,
    'x-ms-client-request-id': str(uuid.uuid4())
}


def create_app():
    try:
        print("Creating enterprise application name: %s" % app_name)
        with open('payloads/create_app.json') as f:
            payload = json.load(f)

        payload.update({
            "displayName": app_name,
            "description": app_description
        })

        s = requests.Session()
        s.headers.update(headers)
        response = s.post(
            api_url + '/GalleryApplications/galleryApplications',
            data=json.dumps(payload))
        response = json.loads(response.content)
        return response['objectId'], response['appId']
    except Exception as e:
        print('Failed to create applicaiton')
        print(e)


def enable_saml(app_objectId):
    try:
        print("Enable SAML SSO for enterprise application")
        payload = {"currentSingleSignOnMode": "federated", "signInUrl": None}

        s = requests.Session()
        s.headers.update(headers)
        response = s.post(
            api_url + '/ApplicationSso/' + app_objectId + '/SingleSignOn',
            data=json.dumps(payload))
        return response.status_code
    except Exception as e:
        print('Failed to enable saml')
        print(e)


def set_saml(app_objectId):
    try:
        print("Setting enterprise application %s saml settings" % app_name)
        with open('payloads/set_saml.json') as f:
            payload = json.load(f)

        payload.update({
            "objectId": app_objectId,
            "certificateNotificationEmail": email,
            "idpReplyUrl": "https://signin.aws.amazon.com/saml",
            "replyUrls": ["https://signin.aws.amazon.com/saml"],
            "idpIdentifier": idp_identifier,
            "identifierUris": [
                idp_identifier,
            ]
        })

        s = requests.Session()
        s.headers.update(headers)
        response = s.post(
            api_url + '/ApplicationSso/' + app_objectId +
            '/FederatedSsoConfigV2',
            data=json.dumps(payload))
        return response.status_code
    except Exception as e:
        print('Failed to set saml settings')
        print(e)


def set_saml_claims(app_objectId):
    try:
        print("Setting enterprise application %s saml claims" % app_name)
        with open('payloads/set_saml.json') as f:
            payload = json.load(f)

        payload.update({
            "objectId": app_objectId,
            "certificateNotificationEmail": email,
            "idpReplyUrl": "https://signin.aws.amazon.com/saml",
            "replyUrls": ["https://signin.aws.amazon.com/saml"],
            "idpIdentifier": idp_identifier,
            "identifierUris": [
                idp_identifier,
            ]
        })

        s = requests.Session()
        s.headers.update(headers)
        response = s.post(
            api_url + '/ApplicationSso/' + app_objectId +
            '/FederatedSsoClaimsPolicyV2',
            data=json.dumps(payload))
        return response.status_code
    except Exception as e:
        print('Failed to set saml claims')
        print(e)


def create_provisioning_template(app_objectId):
    try:
        print("Setting enterprise application %s provisioning template" %
              app_name)
        with open('payloads/create_provisioningtemplate.json') as f:
            payload = json.load(f)
        s = requests.Session()
        s.headers.update(headers)
        response = s.post(
            api_url + '/UserProvisioning/' + app_objectId +
            '/ProvisioningTasks',
            data=json.dumps(payload))
        return response.status_code
    except Exception as e:
        print('Failed to set provisioning template')
        print(e)


def set_aws_creds(app_objectId):
    try:
        print("Setting enterprise application %s aws credentials" % app_name)
        with open('payloads/set_awscredentials.json') as f:
            payload = json.load(f)

        payload['fieldValues'].update({
            "clientsecret": aws_access_key_id,
            "secrettoken": aws_secret_access_key
        })

        s = requests.Session()
        s.headers.update(headers)
        response = s.put(
            api_url + '/UserProvisioning/' + app_objectId + '/Credentials',
            data=json.dumps(payload))
        return response.status_code
    except Exception as e:
        print('Failed to set aws credentials')
        print(e)

def start_provisioning(app_objectId):
    try:
        print("Setting enterprise application %s to start provisioning" % app_name)
        headers.update({'Content-Length': '0'})
        s = requests.Session()
        s.headers.update(headers)
        response = s.post(
            api_url + '/UserProvisioning/' + app_objectId + '/start',
            )
        return response.status_code
    except Exception as e:
        print('Failed to start provisioning')
        print(e)


try:
    app_objectId, app_appId = create_app()
    time.sleep(5)
    if enable_saml(app_objectId) == 204:
        if create_provisioning_template(app_objectId):
            time.sleep(5)
            set_aws_creds(app_objectId)
            time.sleep(15)
            if set_saml(app_objectId) == 204:
                time.sleep(5)
                if set_saml_claims(app_objectId) == 204:
                    time.sleep(5)
                    start_provisioning(app_objectId) 
                    print("Aplication %s with appId: %s created." % (app_name, app_appId))

except Exception as e:
    print("Application %s creation failed" % app_name)
    print(e)

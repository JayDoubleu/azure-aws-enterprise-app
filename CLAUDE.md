# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python-based tool that automates the creation of AWS Enterprise applications on Azure Active Directory. It uses the Azure CLI and REST APIs to configure SAML SSO and user provisioning between Azure AD and AWS.

## Architecture

The application consists of:
- `create.py` - Main script that orchestrates the creation process
- `payloads/` directory containing JSON templates:
  - `create_app.json` - Template for creating the enterprise application
  - `set_saml.json` - SAML configuration settings
  - `create_provisioningtemplate.json` - User provisioning template
  - `set_awscredentials.json` - AWS credential configuration

The script performs these steps in sequence:
1. Creates an enterprise application in Azure AD
2. Enables SAML SSO
3. Creates a provisioning template
4. Sets AWS credentials
5. Configures SAML settings and claims
6. Starts user provisioning

## Commands

### Running the Application
```bash
python create.py --appname "MyApp" --appdesc "Description" --email "admin@example.com" --accountid "123456789012" --accesskey "AKIAIOSFODNN7EXAMPLE" --secretkey "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

### Dependencies
- Requires `azure-cli` installed via pip
- Requires being logged into Azure (`az login`)

### Linting
No specific linting configuration found. Standard Python linting tools like `flake8` or `pylint` can be used.

## Key Implementation Details

- Uses Azure AD's internal API endpoint: `https://main.iam.ad.ext.azure.com/api`
- Requires an Azure access token with resource ID `74658136-14ec-4630-ad9b-26e160ff0fc6`
- Implements delays between API calls to ensure proper resource creation
- All API requests include custom headers with bearer token authentication
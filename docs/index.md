Python:

![image](https://img.shields.io/badge/calver-YYYY.MM.DD-22bfda.svg "CalVer")
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

CI/CD Pipeline:

[![Actions Status](https://github.com/devsetgo/test-api/workflows/Run%20Tests/badge.svg)](https://github.com/devsetgo/test-api/actions)
<!-- [![Actions Status](https://github.com/devsetgo/test-api/workflows/Docker%20RC/badge.svg)](https://github.com/devsetgo/test-api/actions) -->
<!-- [![Actions Status](https://github.com/devsetgo/test-api/workflows/Docker%20Latest/badge.svg)](https://github.com/devsetgo/test-api/actions) -->

SonarCloud:

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_backend-services-api&metric=coverage)](https://sonarcloud.io/dashboard?id=devsetgo_backend-services-api)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_backend-services-api&metric=ncloc)](https://sonarcloud.io/dashboard?id=devsetgo_backend-services-api)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_backend-services-api&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=devsetgo_backend-services-api)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_backend-services-api&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=devsetgo_backend-services-api)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_backend-services-api&metric=security_rating)](https://sonarcloud.io/dashboard?id=devsetgo_backend-services-api)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_backend-services-api&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=devsetgo_backend-services-api)



# Backend-Services-API

Work in progress and not ready for production.

## Objective
- User Management
- Authentication via Token
    - [x] POST Login
    - [x] POST register
    - [x] GET Auth Me
- Users
    - [x] GET List all users
    - [x] GET Count all users
    - [x] GET user ID
    - [x] Post Create User
    - [x] POST Check Password
    - [x] PUT User Status
    - [x] PUT Set User as Admin (Ad)
    - [x] DELETE User ID (Admin Only)
- Health Endpoints (somthing like Spring Actuator)
    - [x] Health
    - [x] Config secure via Authentication
- Tools API
 - [x] XML to JSON
 - [x] JSON to XML


### UML
![UML](images/classes.png "UML of App")
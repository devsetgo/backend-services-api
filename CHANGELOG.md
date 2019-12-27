# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Todo

## [Unreleased]
- websockets (working on it)

## [19.9.27] - 2019-09-27
### Added
- Github Actions complete
  - Test on Push (any branch)
  - Build and Push of Release Candidate Docker Image
  - Build and Push of Latest Docker Image
  - Codecov.io xml update on each run of tests
- README updates for documentation


## [19.9.22] - 2019-09-22
### Added
- Adding Github Actions
  - Test on push
  - docker build for release candidate
  - docker build for master
- adding release-candidate branch as default. Master is now for stable release
- code cleanup of sonarcloud issues found during static scan (Grade A code)
- improved tests and exception testing (still needs some work)
- Update of README documentation
- Docker-Compose file now includes Traefik 2.0 labels

## [19.9.1-beta] - 2019-09-01
### Added
- Hurricane Dorian release.
- Adding Health Endpoints
- Adding tests
- Adding scripts to start tests and run app (dev)

## [19.8.23-beta] - 2019-08-23
### Added
- Additional test to ToDo and User for posting failure

## [19.8.22-beta] - 2019-08-22
### Added
- Cleanup of routers for todo, users, and silly
- Using Starlette Config over python-dotenv
- Testing of endpoints (default, users, todos, silly)
- Adding Password Check to Users endpoint
- Adding Passlib and Bcrypt for hashing of password

### Changed
- Cleanup of routers for todo, users, and silly


## [19.4.20-beta-1] - 2019-04-20
### Added
- routers for todo, users, and silly
- .env file update
- Logging via Loguru

### Changed
- Refactor application
- Changed list to database (SQLite or Postgres)

### Removed
- a lot... due to refactoring
- Removed list for todos
- Some of the Silly endpoints to limit to just list or one user generation

## [19.4.6-beta-1] - 2019-04-06
### Added
- initial commit
- building base frame of project
  - 'User' random data (extension of FastAPI example)
    - Random user contact information
  - 'Item' little change from FastAPI example
  - 'Sample' Generates randomized data
    - can set a delay in seconds (0 -10) as a parameter
    - list can generate from 1 to 1000

### Changed
- Nothing, since it is an initial commit

### Removed
- Nothing, since it is an initial commit

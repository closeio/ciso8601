# Releasing ciso8601 <!-- omit in toc -->

The document will describe the process of releasing a new version of `ciso8601`

<!-- Generated with "Markdown All in One" extension for Visual Studio Code -->
- [Prerequisites](#prerequisites)
- [Create the release artifacts](#create-the-release-artifacts)
- [Create the Git tag](#create-the-git-tag)
- [Create the release in GitHub](#create-the-release-in-github)
- [Reach out to the Close engineering team](#reach-out-to-the-close-engineering-team)
  - [Download the release artifacts](#download-the-release-artifacts)

## Prerequisites

* Confirm that [`VERSION`](setup.py) has been changed
* Confirm that [`CHANGELOG`](CHANGELOG.md) includes an entry for the version
* Confirm that these changes have been merged into the `master`.

## Create the release artifacts

Send a `POST` request to the CircleCI API to trigger the `build_wheels` workflow.

Substitute `$CIRCLE_TOKEN` with your [personal API token](https://app.circleci.com/settings/user/tokens):

```bash
curl --location --request POST 'https://circleci.com/api/v2/project/gh/closeio/ciso8601/pipeline' \
--header 'Circle-Token: $CIRCLE_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
  "branch": "master",
  "parameters": {
    "build_wheels": true
  }
}'
```

## Create the Git tag

Each release is tagged with a Git tag. The tags follow the format `v<version>` (ie. the version with a `v` in front).

For example, version `2.1.3` of `ciso8601` is given the Git tag `v2.1.3`:

```bash
git checkout master
git pull origin master
git tag v2.1.3
git push origin v2.1.3
```

## Create the release in GitHub

Go to https://github.com/closeio/ciso8601/releases/new and draft a new release at the tag you created for the release.

## Reach out to the Close engineering team

Ultimately, it is the [Close](https://close.com/about/) engineering team that uploads the release artifacts to PyPI.
Shoot them an email. (eg. [@thomasst](https://github.com/thomasst) or [@jkemp101](https://github.com/jkemp101))

### Download the release artifacts

Taken from [here](https://circleci.com/docs/2.0/artifacts/#downloading-all-artifacts-for-a-build-on-circleci):

```bash
export CIRCLE_TOKEN=':your_token'

curl -H "Circle-Token: $CIRCLE_TOKEN" https://circleci.com/api/v1.1/project/github/closeio/ciso8601/latest/artifacts \
   | grep -o 'https://[^"]*' \
   | wget --verbose --header "Circle-Token: $CIRCLE_TOKEN" --input-file -
```

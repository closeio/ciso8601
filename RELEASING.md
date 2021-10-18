# Releasing ciso8601 <!-- omit in toc -->

The document will describe the process of releasing a new version of `ciso8601`

<!-- Generated with "Markdown All in One" extension for Visual Studio Code -->
- [Prerequisites](#prerequisites)
- [Create the release in GitHub](#create-the-release-in-github)

## Prerequisites

* Confirm that [`VERSION`](setup.py) has been changed
* Confirm that [`CHANGELOG`](CHANGELOG.md) includes an entry for the version
* Confirm that these changes have been merged into the `master`.
## Create the release in GitHub

1. Go to https://github.com/closeio/ciso8601/releases/new and draft a new release at the tag you created for the release.
2. Each release is tagged with a Git tag. In the `Choose a Tag` field type a new tag. The tag must follow the format `v<version>` (i.e., the version with a `v` in front) (e.g., `v2.2.0`).
3. In the `Release Title` field, type the same tag name (e.g., `v2.2.0`)
4. In the `Describe this release` field copy-paste the `CHANGELOG.md` notes for this release.
5. Click `Publish Release`

This will trigger a [GitHub Action](.github/workflows/build-wheels.yml) that listens for new tags that follow our format, builds the wheels for the release, and publishes them to PyPI.
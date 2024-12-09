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

There is a [GitHub Action](.github/workflows/build-wheels.yml) that must be dispatched manually, which builds the wheels for the release. The artifacts can then be downloaded locally then [uploaded to pypi](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#upload-your-distributions).

The `dist/` folder should look roughly like:
```
$ ls dist
ciso8601-2.3.2-cp310-cp310-macosx_11_0_arm64.whl
ciso8601-2.3.2-cp310-cp310-macosx_11_0_universal2.whl
...
ciso8601-2.3.2-pp39-pypy39_pp73-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl
ciso8601-2.3.2.tar.gz
```

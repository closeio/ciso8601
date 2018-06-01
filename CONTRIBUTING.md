# Contributing to ciso8601

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to ciso8601, which are hosted in the [Close.io Organization](https://github.com/closeio) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[I don't want to read this whole thing, I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)

* [Design Philosophy](#design-philosophy)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Developing ciso8601 code](#developing-ciso8601-code)
    * [General Workflow](#general-workflow)
    * [C Coding Style](#c-coding-style)
    * [Supported Python Versions](#supported-python-versions)
    * [Supported Operating Systems](#supported-operating-systems)
    * [Functional Testing](#functional-testing)
    * [Performance Benchmarking](#performance-benchmarking)
    * [Documentation](#documentation)
    * [Pull Requests](#pull-requests)

## I don't want to read this whole thing I just have a question!!!

Sure. First [search the existing issues](https://github.com/closeio/ciso8601/issues?utf8=%E2%9C%93&q=is%3Aissue) to see if one of the existing issues answers it. If not, simply [create an issue](https://github.com/closeio/ciso8601/issues/new) and ask your question.

## Design Philosophy

ciso8601's goal is to be the fastest ISO 8601 parser available for Python. It probably will never support the complete grammar of ISO 8601, but it will be correct for the chosen subset of the grammar. It will also be robust against non-conforming inputs. Beyond that, performance is king. 

That said, some care should still be taken to ensure cross-platform compatibility and maintainability. For example, this means that we do not hand-code assembly instructions for a specific CPUs/architectures, and instead rely on the native C compilers to take advantage of specific hardware. We are not against the idea of platform-specific code in principle, but it would have to be shown to be produce sufficient benefits to warrant the additional maintenance overhead.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for ciso8601. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.

Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report).

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

* **Perform a [cursory search](https://github.com/closeio/ciso8601/issues?utf8=%E2%9C%93&q=is%3Aissue)** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on the repository and provide the following information.

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include snippets of code that reproduce the problem (Make sure to use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines) so that it gets formatted in a readable way).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version of ciso8601 are you using?** You can get the exact version by running `pip list` in your terminal. If you are not using [the latest version](https://github.com/closeio/ciso8601/releases), does the problem still happen in the latest version?
* **What's the name and version of the OS you're using**?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for ciso8601, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:.

Before creating enhancement suggestions, please check [this list](#before-submitting-an-enhancement-suggestion) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion).

#### Before Submitting An Enhancement Suggestion

* **Perform a [cursory search](https://github.com/closeio/ciso8601/issues?utf8=%E2%9C%93&q=is%3Aissue)** to see if the enhancement has already been suggested. 

If it has, don't create a new issue. Consider adding a :+1: [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the issue description. If you feel that your use case is sufficiently different, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on the repository and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to most ciso8601 users and therefore should be implemented in ciso8601.
* **List some other libraries where this enhancement exists** (if you know of any).
* **Specify which version of ciso8601 you're using.** You can get the exact version by running `pip list` in your terminal. If you are not using [the latest version](https://github.com/closeio/ciso8601/releases), is the enhancement still needed in the latest version?
* **Specify the name and version of the OS you're using.**

### Developing ciso8601 code

#### General Workflow

ciso8601 uses the same contributor workflow as many other projects hosted on GitHub.

1. Fork the [ciso8601 repo](https://github.com/closeio/ciso8601) (so it becomes `yourname/ciso8601`).
1. Clone that repo (`git clone https://github.com/yourname/ciso8601.git`).
1. Create a new branch (`git checkout -b my-descriptive-branch-name`).
1. Make your changes and commit to that branch (`git commit`).
1. Push your changes to GitHub (`git push`).
1. Create a Pull Request within GitHub's UI.

See [this guide](https://opensource.guide/how-to-contribute/#opening-a-pull-request) for more information about each step.

#### C Coding Style

ciso8601 tries to adhere to the [Python PEP 7](https://www.python.org/dev/peps/pep-0007/) style guide. 

You can use [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html) to make this mostly automatic. The auto-formatting rules are defined in the [.clang-format](.clang-format) file. If you are using Visual Studio Code as your editor, you can use the ["C/C++"](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) extension and it will automatically start auto-formatting.

#### Supported Python Versions

ciso8601 supports a variety of cPython versions, including Python 2.7 (for the full list see the [README](README.rst)). Please make sure that you do not accidentally make use of features that are specific to certain versions of Python. Feel free to make use of modern features of the languages, but you also need to provide mechanisms to support the other versions as well.

You can make use of `#ifdef` blocks within the code to make use of version specific features (there are already several examples throughout the code).   

#### Supported Operating Systems

ciso8601 supports running on multiple operating systems, including Windows. Notably, for Python 2.7 on Windows, the compiler (MSVC) places additional restrictions on the C language constructs you can use. Make sure to test changes on both a Windows (MSVC) and Linux (gcc) machine to ensure compatibility.

#### Functional Testing

ciso8601's functionality/unit tests are found in the [tests.py](tests.py) file. The [`tox`](https://tox.readthedocs.io/en/latest/) command can be used to run the tests:

```bash
pip install tox
...
tox
```

This will automatically run [nosetests](https://nose.readthedocs.io/en/latest/man.html) command (as specified in the [`tox.ini`](tox.ini) file) to find and run all the tests. Make sure that you have at least the latest stable Python 3 interpreter and the latest Python 2.7 interpreter installed.

Any new functionality being developed for ciso8601 should also have tests being written for it. Tests should cover both the "sunny day" (expected, valid input) and "rainy day" (invalid input or error) cases.

Many of ciso8601's functionality tests are auto-generated. The code that does this generation is found in the [`generate_test_timestamps.py`](generate_test_timestamps.py) file. It can sometimes be useful to print out all of the test cases and their expected outputs:

```python
from generate_test_timestamps import generate_valid_timestamp_and_datetime

for timestamp, expected_datetime in generate_valid_timestamp_and_datetime():
    print("Input: {0}, Expected: {1}".format(timestamp, expected_datetime))
```

#### Performance Benchmarking

The ciso8601 project was born out of a need for a fast ISO 8601 parser. Therefore the project is concerned with the performance of the library.

Changes should be assessed for their performance impact, and the results should be included as part of the Pull Request.

#### Documentation

All changes in functionality should be documented in the [`README.rst`](README.rst) file. Note that this file uses the [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) format, since the file is rendered as part of [ciso8601's entry in PyPI](https://pypi.org/project/ciso8601/), which only supports reStructuredText.

You can check your reStructured text for syntax errors using (restructuredtext-lint)[https://github.com/twolfson/restructuredtext-lint]:

```
pip install Pygments restructuredtext-lint
rst-lint --encoding=utf-8 README.rst
```

#### Pull Requests

* Follow the [C Code](#c-coding-style) style guide.
* Document new code and functionality [See "Documentation"](#documentation)


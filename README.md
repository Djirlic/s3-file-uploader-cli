# 📤 s3-file-uploader-cli

[![codecov](https://codecov.io/gh/Djirlic/s3-file-uploader-cli/graph/badge.svg?token=7DVWY9HMKG)](https://codecov.io/gh/Djirlic/s3-file-uploader-cli)
![CI](https://github.com/Djirlic/s3-file-uploader-cli/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)

A Python CLI tool to upload files to an AWS S3 bucket using a presigned URL. Designed for data engineering workflows, automation pipelines, and robust CLI-based file ingestion.

Built with portability, reproducibility, and cloud-native best practices in mind.

---

## 🚀 Features

- Upload any file to S3 via presigned URL.
- AWS authentication via named profile (from `~/.aws/credentials`).
- Supports dynamic S3 bucket names and upload paths.
- Well-structured CLI with helpful error messages and validation.
- Fully typed and tested Python codebase.
- Compatible across macOS, Linux, and Windows.

---

## ⚠️ Limitations

- The maximum supported file size is **5 GB**, due to the use of presigned URLs with S3 `put_object` operations.
- Multipart uploads (required for files >5 GB) are not yet supported.
- Uploads are unauthenticated beyond the presigned URL — anyone with the URL can upload during its validity period (300 seconds).
- No built-in retry or resumable uploads — transient network issues may cause failures.
- The CLI assumes the AWS profile is configured locally (via `~/.aws/credentials`).

---

## ✅ Prerequisites

Before using this tool, make sure the following are set up:

- **Python 3.13+** installed on your system
- An **AWS S3 bucket** you have access to (create one if needed)
- An **AWS CLI** installation and configuration:
  - [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
  - Run `aws configure` to set up your credentials
- An **AWS profile** properly configured in `~/.aws/credentials` and `~/.aws/config`:
  - You can use the default profile or a named profile via `--profile` when using this tool

> [!WARNING]
> For safety and best practices, we strongly recommend using an **AWS profile with least privilege** when running this tool.
> This means:
> - Create a dedicated IAM user or role for uploads
> - Attach a custom policy that **only allows `s3:PutObject` on the specific bucket or path**
> - Avoid using your root credentials or overly permissive policies like `AdministratorAccess`
>
> This reduces the risk of accidental or malicious access to other AWS resources in your account.

---

## 📦 Installation

Clone the repo and install dependencies using Poetry:

```bash
poetry install --with dev,test
```

Alternatively, you can use:

```bash
make install
```

You’ll also need to have Python 3.13+ installed.

---

## ⚙️ Usage

Run the CLI:

```bash
poetry run python -m uploader.main \
  --bucket-name my-bucket-name \
  --upload-path uploads/my-file.csv \
  --file-location ~/Downloads/local-file.csv \
  --profile default
```

Or alternatively:

```bash
make run ARGS="--bucket-name my-bucket-name \
  --upload-path uploads/my-file.csv \
  --file-location ~/Downloads/local-file.csv \
  --profile default"
```

Arguments:

- `--bucket-name`: Target S3 bucket to upload to (required)
- `--upload-path`: S3 key where file should be stored (required)
- `--file-location`: Path to the local file to upload (required)
- `--profile`: AWS CLI profile to use (optional, defaults to `default`)

---

## 🧪 Testing & Coverage

Run all tests:

```bash
make test
```

Generate test coverage report:

```bash
make test-coverage
```

---

## 🧼 Code Style & Quality

This project uses the following tools:

- `black` for formatting
- `flake8` for linting
- `isort` for sorting imports
- `mypy` for type checks
- `pre-commit` to run all tools automatically before each commit

Run pre-commits without a commit:

```bash
pre-commit run --all-files
```

---

## 📁 Project Structure

```
s3-file-uploader-cli/
├── src/
│   └── uploader/           # Main logic (presign, upload, logging)
├── tests/                  # Unit tests for all modules
├── .github/workflows/     # CI pipeline with linting + test coverage
├── .pre-commit-config.yaml
├── Makefile                # Common tasks (run, test, lint, etc)
├── pyproject.toml          # Tooling config (Poetry, mypy, black, etc)
```

---

## 📌 Future Improvements

- Support multi-part uploads for large files.
- Add retry and backoff logic on upload failures.
- Add logging hooks to external monitoring systems.
- Add support for directory-level uploads.

---

Feel free to fork, contribute, or reach out if you find this project helpful! 🙌

# COCO Processing & Upload Scripts

<!--
Filename: README.md
Purpose: Documentation for COCO preprocessing and upload scripts
-->

This repository contains **two Python scripts** used in the COCO annotation workflow:

1. `process_coco_file.py` – cleans and standardizes a COCO JSON file
2. `upload_coco_file_to_darwin.py` – uploads the processed COCO file using an AWS SageMaker processing job

These scripts are typically used **sequentially**:

> **Step 1:** Clean and normalize the COCO file locally
> **Step 2:** Upload the cleaned COCO file to the Darwin/AIDA pipeline via SageMaker

---

## 1. `process_coco_file.py`

### Purpose

This script prepares a raw COCO JSON file for downstream pipelines by:

* Renaming the non‑standard key `taqadam_filename` → `file_name`
* Cleaning category names by:

  * Removing the prefix `Labels - `
  * Capitalizing each word for consistency

This ensures compatibility with tools that expect standard COCO field names and clean category labels.

---

### What the Script Does

#### 1. Rename `taqadam_filename`

Some COCO exports contain a non‑standard key called `taqadam_filename`.
The script replaces **all occurrences** of this key with the standard COCO key `file_name`, even if it appears in nested structures.

#### 2. Normalize Category Names

Category names are cleaned using the following rules:

| Original Name           | Cleaned Name   |
| ----------------------- | -------------- |
| `Labels - corner break` | `Corner Break` |
| `Labels - patch`        | `Patch`        |

---

### How It Works

* Loads the COCO JSON file
* Converts it temporarily to a string to safely replace all key occurrences
* Iterates through the `categories` list and cleans each category name
* Saves a **new formatted COCO file** with proper indentation

---

### Usage

```bash
python process_coco_file.py
```

By default, the script is executed from the `__main__` block:

```python
if __name__ == "__main__":
    update_coco_file(
        input_path="/Users/oreyeon/Desktop/NRV1104.coco.json",
        output_path="/Users/oreyeon/Desktop/NRV1104.json"
    )
```

Update the paths above to match your local environment.

---

### Output

* A cleaned and standardized COCO JSON file
* Properly indented and ready for upload

---

## 2. `upload_coco_file_to_darwin.py`

### Purpose

This script uploads a COCO file to the Darwin/AIDA pipeline by launching an **AWS SageMaker Processing Job** using a custom Docker image.

It is typically used **after** the COCO file has been cleaned using `process_coco_file.py`.

---

### What the Script Does

* Creates a SageMaker processing job
* Mounts a COCO file from an S3 bucket into the container
* Passes batch‑level arguments to the container
* Triggers the upload logic inside the Docker image

---

### Required Arguments

The processing container expects the following arguments:

```python
processor_args = [
    "--batch_id", batch_id,
    "--coco_id", coco_id
]
```

> Replace `batch_id` and `coco_id` with the correct identifiers before running the script.

---

### Key Configuration

| Parameter              | Description                                  |
| ---------------------- | -------------------------------------------- |
| `IMAGE_URI`            | Docker image that handles COCO upload        |
| `ROLE_ARN`             | SageMaker execution role                     |
| `INSTANCE_TYPE`        | EC2 instance type used for processing        |
| `S3Uri`                | S3 path to the COCO file                     |
| `CONTAINER_INPUT_PATH` | Path where COCO file is mounted in container |

---

### Example S3 Input Configuration

```python
"S3Uri": "s3://oreyeon-models/yolov5/coco-haivo-new/NRV1099.json"
```

Replace this path with the S3 URI of the cleaned COCO file you want to upload.

---

### How to Run

```bash
python upload_coco_file_to_darwin.py
```

Once executed, the script:

* Generates a unique processing job name
* Starts the SageMaker job
* Uploads the COCO file via the container

---

### Output

* A SageMaker processing job visible in AWS console
* COCO annotations uploaded and registered in the Darwin/AIDA system

---

## Recommended Workflow

```text
Raw COCO JSON
      ↓
process_coco_file.py
      ↓
Cleaned COCO JSON
      ↓
Upload to S3
      ↓
upload_coco_file_to_darwin.py
      ↓
COCO available in Darwin / AIDA
```

---



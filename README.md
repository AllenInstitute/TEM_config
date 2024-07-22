# openTEM Deployment Config Generator

This project provides a script to materialize openTEM configuration files to create a docker-compose.yaml file from Jinja2 templates using settings defined in environment variable files.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
  - [Make a new deployment](#make-a-new-deployment)  
  - [One-Off Generation Using Environment Variables](#one-off-generation-using-environment-variables)

## Prerequisites


Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Directory Structure

```.
├── environments # microscope settings dir
│   ├── specific-microscope
│   │   └── settings.env # setting for 'specific-microscope'
│   ├── another-microscope
│   │   └── settings.env
├── output
│   └── specific-microscope # materialized files
│   │   └── docker-compose.yaml
│   │   └── TEM_graph.yaml
│   │   └── ximea.yaml
│   │   └── pytem.yaml
│   │   └── another_template.yaml
│   └── another-microscope
├── templates
│   ├── docker-compose.yaml.j2
│   ├── TEM_graph.yaml.j2
│   ├── ximea.yaml.j2
│   └── pytem.yaml.j2
│   └── another_template.yaml.j2
├── scripts
│   └── materialize_templates.py
└── README.md
```

Note that the output directory is ignored in the repository as it is a transient file that is generated with the scripts.

## Usage

The main script will generate both config files for each service defined as well as a service in a docker-compose.yaml file. The user can define image versions of each deployment as well as the required config params to run the service.

### Make a new deployment

Create a new settings.env file in the environments/name_of_your_microscope directory. To do so run the following script:

```bash
python scripts/create_default_settings_env.py --env-name 'name_of_your_env'
```

Navigate to /environments/name_of_your_env/settings.env and
modify it with the required parameters for each template you wish to materialize.


### One-Off Generation Using Environment Variables

1. Confirm that an .env file with your settings (e.g., environments/name_of_your_env/settings.env) exists.

2. Run the script:

```bash
python scripts/materialize_templates.py --env-file environments/name_of_your_env/settings.env --output-dir output/name_of_your_env
```

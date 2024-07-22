import yaml
import argparse
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

env = Environment(loader=FileSystemLoader('templates'))

def generate_config(template_name, output_path, context):
    template = env.get_template(template_name)
    rendered_content = template.render(context)
    output_path.write_text(rendered_content)

def load_yaml_settings(settings_file):
    with settings_file.open('r') as f:
        return yaml.safe_load(f)

def convert_value(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    return value

def load_env_settings(env_file):
    load_dotenv(dotenv_path=env_file)
    return {key.lower(): convert_value(value) for key, value in os.environ.items()}

def generate_configs(settings, output_dir, template_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    template_files = list(template_dir.glob('*.j2'))
    
    for template_file in template_files:
        template_base_name = template_file.name
        output_file_name = template_base_name.replace('.j2', '')
        output_path = output_dir / output_file_name
        
        context = settings
        generate_config(template_file.name, output_path, context)

def main():
    parser = argparse.ArgumentParser(description='Generate configuration files from templates.')
    parser.add_argument('--env-file', type=Path, help='Path to the .env file for one-off generation')
    parser.add_argument('--output-dir', type=Path, required=True, help='Directory to save the generated configuration files')
    parser.add_argument('--templates-dir', type=Path, default=Path('templates'), help='Directory containing the Jinja2 templates')
    
    args = parser.parse_args()
    
    try:
        settings = load_env_settings(args.env_file)
        generate_configs(settings, args.output_dir, args.templates_dir)
    except Exception as e:
        print(f"Error generating configuration files: {e}")
        return
    
    print("Configuration files generated successfully!")

if __name__ == '__main__':
    main()

import os
from pathlib import Path

def create_default_settings_env(env_name):
    script_dir = Path(__file__).resolve().parent
    # go up one directory to the root of the project
    base_dir = script_dir.parent / 'environments'

    print(base_dir)
    env_dir = base_dir / env_name   
    
    try:
        env_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"PermissionError: {e}. Please ensure you have the necessary permissions to create directories in the specified path.")
        return
    except Exception as e:
        print(f"Error: {e}.")
        return
        

    env_file = env_dir / 'settings.env'
    
    default_settings = {
        "INCLUDE_XIMEA": "true",

        "BROKER_IMAGE": "apache/activemq-artemis",
        "BROKER_VERSION": "latest",
        "BROKER_ANONYMOUS_LOGIN": "true",
        "BROKER_PORT1": "61616:61616",
        "BROKER_PORT2": "8161:8161",
        "BROKER_HEALTHCHECK_TIMEOUT": "15s",
        "BROKER_HEALTHCHECK_START_PERIOD": "10s",
        "BROKER_HEALTHCHECK_URL": "http://localhost:8161/",

        "PYTEM_IMAGE": "your_pytem_image",
        "PYTEM_VERSION": "v1.0.0",
        "PYTEM_COMMAND": "pigeon-transitions --host broker /config/pytem.yaml",
        "PYTEM_DEPENDS_ON_XIMEA": "service_healthy",
        "PYTEM_DEPENDS_ON_CONFIG": "service_completed_successfully",

        "TEM_GRAPH_IMAGE": "your_tem_graph_image",
        "TEM_GRAPH_VERSION": "v1.0.0",
        "TEM_GRAPH_COMMAND": "TEM_graph /config/tem_graph.yaml",
        "TEM_GRAPH_DEPENDS_ON_CONFIG": "service_completed_successfully",
        "TEM_GRAPH_DEPENDS_ON_BROKER": "service_healthy",
        "TEM_GRAPH_DRIVER": "nvidia",
        "TEM_GRAPH_COUNT": "all",
        "TEM_GRAPH_CAPABILITIES": "gpu",

        "XIMEA_IMAGE": "your_ximea_image",
        "XIMEA_VERSION": "v1.0.0",
        "XIMEA_COMMAND": "XIMEA_service --host broker /config/ximea.yaml",
        "XIMEA_DEVICE": "/dev/ximea00:/dev/ximea00",
        "XIMEA_DEPENDS_ON_BROKER": "service_healthy",
        "XIMEA_DEPENDS_ON_CONFIG": "service_completed_successfully",
        "XIMEA_HEALTHCHECK_START_PERIOD": "10s",
        "XIMEA_HEALTHCHECK_TEST": "timeout 5s pigeon --host broker -s camera.status --one || exit 1",

        "CONFIG_VOLUME": f"output/{env_name}:/config",
        "TMP_VOLUME": "/tmp:/tmp",

        "XIMEA_IMAGE_SIZE": "1024",
        "XIMEA_OUTPUT_DIR": "/data/output",
        "XIMEA_GAIN": "1.0",
        "XIMEA_DUMMY": "false"
    }
    
    with env_file.open('w') as f:
        for key, value in default_settings.items():
            f.write(f"{key}={value}\n")
    
    print(f"Default settings.env created at {env_file}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Create a default settings.env file in the specified environments directory.')
    parser.add_argument('--env-name', type=str, required=True, help='Name of the new environment directory')
    
    args = parser.parse_args()
    
    create_default_settings_env(args.env_name)

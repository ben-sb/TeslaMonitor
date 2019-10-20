from classes.monitor import Monitor
import json


if __name__ == '__main__':
    try:
        config = json.load(open('config.json'))

        monitor = Monitor(model=config['model'], condition=config['condition'], delay_in_seconds=int(config['refresh_delay']))
        monitor.run()

    except FileNotFoundError:
        print("FATAL ERROR: Could not find config file")

    # case where config file is not valid json
    except json.decoder.JSONDecodeError:
        print("FATAL ERROR: Could not read config file, invalid JSON")

    # case where we don't know the cause of the exception
    except Exception as e:
        print("Unknown error: " + str(e))



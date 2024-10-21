import logging
import multiprocessing
import os
import socket
import subprocess


BACK_END_DIR = 'back_end'
BACK_END_PORT = 5000
FRONT_END_DIR = 'front_end'
FRONT_END_PORT = 8000

logger = logging.getLogger()


def run_back_end():
    """Run the back-end flask service"""
    os.chdir(BACK_END_DIR)
    subprocess.run(['python', 'service.py', '--port', BACK_END_PORT])


def run_front_end():
    """Run an HTTP server to serve front-end files."""
    os.chdir(FRONT_END_DIR)
    subprocess.run(['python', '-m', 'http.server', str(FRONT_END_PORT)])


def run_application(processes):
    """Run the application defined by processes."""
    for name, process in processes.items():
        logger.info(f"Starting {name} process.")
        process.start()
        logger.info(f"Started {name} process.")
    
    return processes

    
def terminate_process(process):
    """Terminate a process."""
    process.terminate()
    process.join()


def terminate_application(processes):
    """Terminate all processes in the application."""
    for name, process in reversed(processes.items()):
        logger.info(f"Terminating {name} process.")
        terminate_process(process)
        logger.info(f"Terminated {name} process.")


def build_application():
    """Build the application."""
    back_end_process = multiprocessing.Process(target=run_back_end)
    front_end_process = multiprocessing.Process(target=run_front_end)
    
    processes = dict(
        back_end=back_end_process,
        front_end=front_end_process,
    )
    
    for name, process in processes.items():
        logger.info('Initialized process {name!r}.')

    return processes


def idle_loop():
    """Loops idly forever."""
    ctrl_c_pressed = False
    while not ctrl_c_pressed:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ctrl_c_pressed = True


def init_logging():
    """Initialize logging."""
    log_level = logging.DEBUG
    log_format = (
        '[%(asctime)s] '
        '[%(levelname)s] '
        '[%(name)s] '
        '[%(filename)s:%(lineno)d] '
        '--- '
        '%(message)s'
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
    )


def main():
    """Prepare, configure, and run the application."""
    success, failure = 0, -1
    
    init_logging()
    
    exit_code = failure
    try:
        processes = build_application()
        run_application(processes)
        idle_loop()
        terminate_application(processes)
        exit_code = success
    except:
        logger.exception(f'An unexpected error occurred.')
    
    return exit_code


if __name__ == '__main__':
    exit(main())

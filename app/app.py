from flask import Flask, render_template, Response
import subprocess
import sys
import threading
import time


app = Flask(__name__)

# Global buffer and a lock for thread-safety
log_buffer = []
log_lock = threading.Lock()

# Global variables for the controller process and controller thread
controller_process = None
controller_thread = None  # Initialize controller_thread



def run_controller():
    # Launch the controller process once (it will keep running even if the page is reloaded)
    controller_process = subprocess.Popen(
        [sys.executable, "controller.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    # Continuously read output from the process and store in buffer
    for line in iter(controller_process.stdout.readline, ""):
        with log_lock:
            log_buffer.append(line)
    controller_process.stdout.close()
    controller_process.wait()


# Start the controller process as a background thread
def start_controller_thread():
    global controller_thread
    # Start only if not already running
    if controller_thread is None or not controller_thread.is_alive():
        controller_thread = threading.Thread(target=run_controller, daemon=True)
        print("Controller start")
        controller_thread.start()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controller-view')
def controller_view():
    start_controller_thread()
    return render_template('controller-view.html')

@app.route('/stream')
def stream():
    def generate():
        last_index = 0
        while True:
            time.sleep(0.5)
            with log_lock:
                # If there are new log entries, grab them
                if last_index < len(log_buffer):
                    new_lines = log_buffer[last_index:]
                    last_index = len(log_buffer)
                else:
                    new_lines = []
            for line in new_lines:
                # Yield each new line as an SSE event
                yield f"data:{line}\n\n"

    return Response(generate(), mimetype='text/event-stream')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
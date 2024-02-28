# Thanks, ChatGPT!
from flask import Flask, request, make_response
import subprocess
import os
import uuid
import gzip

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_sequence():
    if request.method == 'POST':
        sequence = request.form['sequence']

        # Generate a unique filename to avoid conflicts
        filename = f"{uuid.uuid4()}.txt"
        local_path = os.path.join('tmp', filename)

        with open(local_path, 'w') as file:
            file.write(sequence)

        # Define the remote path
        remote_path = '/path/to/destination/'
        remote_file = f"{remote_path}{filename}"

        # Ensure the remote directory exists
        mkdir_command = f"ssh user@compute-server 'mkdir -p {remote_path}'"
        subprocess.run(mkdir_command, shell=True)

        # SCP to transfer the file to the compute server
        scp_command = f"scp {local_path} user@compute-server:{remote_file}"
        subprocess.run(scp_command, shell=True)

        # SSH to execute the command on the compute server
        command_on_server = f"ssh user@compute-server 'command-to-run {remote_file}'"
        subprocess.run(command_on_server, shell=True)

        # SCP to retrieve the gzipped result
        result_filename_gz = f"result_{filename}.gz"
        result_local_path_gz = os.path.join('tmp', result_filename_gz)
        result_remote_file_gz = f"{remote_path}{result_filename_gz}"
        scp_command_result = f"scp user@compute-server:{result_remote_file_gz} {result_local_path_gz}"
        subprocess.run(scp_command_result, shell=True)

        # Unzip the result file
        result_local_path = os.path.join('tmp', f"result_{filename}")
        with gzip.open(result_local_path_gz, 'rb') as f_in:
            with open(result_local_path, 'wb') as f_out:
                f_out.write(f_in.read())

        # Serve the result as plain text
        with open(result_local_path, 'r') as file:
            result = file.read()

        response = make_response(result, 200)
        response.mimetype = "text/plain"
        return response

    return '''
    <!doctype html>
    <title>Upload Sequence</title>
    <h1>Upload a sequence</h1>
    <form method=post>
      <textarea name=sequence></textarea>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)


# Thanks, ChatGPT!
from flask import Flask, request, make_response
import subprocess
import os
import uuid

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
        
        # SCP to transfer the file to the compute server
        scp_command = f"scp {local_path} user@compute-server:/path/to/destination/{filename}"
        subprocess.run(scp_command, shell=True)
        
        # SSH to execute the command on the compute server
        command_on_server = f"ssh user@compute-server 'command-to-run /path/to/destination/{filename}'"
        subprocess.run(command_on_server, shell=True)
        
        # SCP to retrieve the result
        result_filename = f"result_{filename}"
        scp_command_result = f"scp user@compute-server:/path/to/result/{result_filename} {local_path}"
        subprocess.run(scp_command_result, shell=True)
        
        # Serve the result as plain text
        with open(local_path, 'r') as file:
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


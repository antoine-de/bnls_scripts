
## Simple
To run the simple normalize script, install dependencies (python3 needed):
`pip install -r requirements.txt`

then:
`python normalize.py cleanup_addr <input_file> <output_file>`

## Docker
the script in docker is way more complex as it uses [libpostal](https://github.com/openvenues/libpostal) and [reaccentue](https://github.com/cquest/reaccentue). It's thus more generic than the simple script, but for our use case (only french data) it is way overkill. 


To run it:

`docker build -t bnls_scripts .  && docker run -v <directory_with_data>/:/data --rm bnls_scripts cleanup_addr /data/<data_file_name>`

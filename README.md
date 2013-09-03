Process Registry
================


A basic prototype Process Registry.

Installation
------------

Use the setup.py to install. The settings.py file is configured to use sqlite by
default. If you want to use mysql, refer to the standard instructions for 
databases (https://docs.djangoproject.com/en/dev/ref/settings/#databases) on
the Django documentation site.

Usage
-----

To query, the process registry, you can do GET/POST/PUT/DELETE against

    /api/process_definition/ 

to do standard Create/Update/Read/Delete operations.

For example to get a list of records:

    $ curl -u $USERNAME:$PASSWORD http://127.0.0.1:8000/api/process_definition/
    {
      "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 2
      },
      "objects": [
        {
          "definition": {
            "exec": "/path/to/executable"
          },
          "id": 1,
          "resource_uri": "/api/process_definition/1/"
        },
        {
          "definition": {
            "exec": "/path/to/executable"
          },
          "id": 2,
          "resource_uri": "/api/process_definition/2/"
        }
      ]
    }

To create a process definition:

    $ curl -u $USERNAME:$PASSWORD --dump-header - -H "Content-Type: application/json" -X POST --data '{"definition": {"exec": "/path/to/executable"}}' http://localhost:8000/api/process_definition/
    HTTP/1.0 201 CREATED
    Date: Wed, 28 Aug 2013 18:19:43 GMT
    Server: WSGIServer/0.1 Python/2.7.2
    Vary: Accept
    Content-Type: text/html; charset=utf-8
    Location: http://localhost:8000/api/process_definition/3/

etc.

Process Definition Format
-------------------------

The basic Process Definition format is a dictionary like the following:

    {
        "exec": "/path/to/executable",
        "application": "referencetodtindtrs",
        "process_type": "typeofprocess",
        "timeout": 60,
        "cwd": "/path/to/cwd",
        "environment": {"ENVAR": "val},
        "argv": ["arg1", "arg2"],
        "input_adapter": {
            "input_type": "intype",
            "input_params": {
                "chunk_size": "10KB",
                "tcp_port": 8090
            }
        },
        "output_adapter" {
            "output_type": "outtype",
            "output_params": {
                 "file": "path/to/file"
            }
        }

    }

With the following parameters:

**exec**: Path to the executable that should be run
**application**: Reference to the application that this runs on. This is a DT in the DTRS, which includes the VM image it will run on, and the chef recipes / configuration that needs to be installed
**process_type**: Type of process. Choose from:
* *single*: a process that takes an input file, and produces an output (think gcc)
* *service*: a process that runs for a long time

**cwd**: Current working directory of executable
**environment**: Environment variables that should be set for a process
**argv**: List of arguments that should be passed to the process
**input_adapter**: Defines a way of moving data from the messaging system to the process. A dictionary that can take the following parameters:
* *input_type*: The type of input that the process expects, could be a single file that is read once, input to a port, appending to a file, writing to a unix pipe, etc.
* *input_parameters*: Depends on the input type, but a dictionary of parameters to configure the input adapter

**output_adapter**: Defines a way of moving data produced by the process to the messaging system. A dictionary that can take the following parameters:
* *output_type*: The type of output that the process produces, could be a single file, output read from a port, a file that is appended to, a unix pipe that can be read, etc.
* *output_parameters*: Depends on the output type, but a dictionary of parameters to configure the output adapter


Input and Output Adapters
-------------------------

Since the ways in which processes get input and produce output is widely varied, we need an extensible and flexible way of defining how to adapt messages from the messaging framework to be fed to a process, and a way of reading the output produced from that process and put on the messaging framework. Some examples:

### Input

**file**: A simple file that is fed to a process. The message is written to a file, and then fed somehow to the process, either by standard input or as an argument to the process.

For example, a file that is fed by STDIN:


    {
        "exec": "someproc",
        "input_adapter": {
             "input_type": "file",
             "input_parameters": {
                 "file_type": "stream",
                 "stream_name": "STDIN"
             }
        }
    }

This produces the equivalent of:

    $ someproc < /path/to/file


Another example, a file that is fed by trailing argument:


    {
        "exec": "someproc",
        "args": ["--quiet", "--input", "${input_file}"],
        "input_adapter": {
            "input_type": "file",
            "input_parameters": {
                "file_path": "${input_file}"
            }
        }
    }


This produces the equivalent of:

    $ someproc --quiet --input /path/to/file


### Output

*file*: A simple file that is produced by a process. The file is read from the process somehow, either from stdout or an a.out style file, and then is put on the message bus:

For example, a file that is read from STDOUT:


    {
        "exec": "someproc",
        "output_adapter": {
            "output_type": "file",
            "output_parameters": {
                "file_type": "stream",
                "stream_name": "STDOUT"
            }
        }
    }


This produces the equivalent of:

    $ someproc > /path/to/file


Another example, a file that is produced by trailing argument:


    {
        "exec": "someproc",
        "args": ["--quiet", "${output_file}"],
        "output_adapter": {
            "output_type": "file",
            "output_parameters": {
                "file_path": "${output_file}"
            }
        }
    }


This produces the equivalent of:

    $ someproc --quiet --output /path/to/file


### Practical Example: tr

tr is a simple text stream transformation process. We will use it to apply a simple transformation process to a text stream where we remove every 'x' character. Here is an example process configuration for it:


    {
        "exec": "/usr/bin/tr",
        "argv": ["-d", "x"],
        "input_adapter": {
            "input_type": "file",
            "input_parameters": {
                "file_type": "stream",
                "stream_name": "STDIN"
            }
        },
        "output_adapter": {
            "output_type": "file",
            "output_parameters": {
                "file_type": "stream",
                "stream_name": "STDOUT"
            }
        }
    }


### Practical Example: ffmpeg

ffmpeg is a tool to convert and stream audio and video. In this example, we will encode an audio sample into the MP3 format.


    {
        "exec": "/usr/local/bin/ffmpeg",
        "argv": ["-i", "${input_file}", "-q:a", "2", "${output_file}"],
        "input_adapter": {
            "input_type": "file",
            "input_parameters": {
                "file_path": "${input_file}"
            }
        },
        "output_adapter": {
            "output_type": "file",
            "output_parameters": {
                "file_path": "${output_file}"
            }
        }
    }

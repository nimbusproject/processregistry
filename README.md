Process Registry
================


A basic prototype Process Registry.

INSTALLATION
============

Use the setup.py to install. The settings.py file is configured to use sqlite by
default. If you want to use mysql, refer to the standard instructions for 
databases (https://docs.djangoproject.com/en/dev/ref/settings/#databases) on
the Django documentation site.

USAGE
=====

To query, the process registry, you can do GET/POST/PUT/DELETE against the

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

PROCESS DEFINITION FORMAT
=========================

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

*exec*: Path to the executable that should be run
*application*: Reference to the application that this runs on. This is a DT in the DTRS, which includes the VM image it will run on, and the chef recipes / configuration that needs to be installed
*process_type*: Type of process. Choose from:
* _single_: a process that takes an input file, and produces an output (think gcc)
* _service_: a process that runs for a long time

*cwd*: Current working directory of executable
*environment*: Environment variables that should be set for a process
*argv*: List of arguments that should be passed to the process
*input_adapter*: Defines a way of moving data from the messaging system to the process. A dictionary that can take the following parameters:
* _input_type_: The type of input that the process expects, could be a single file that is read once, input to a port, appending to a file, writing to a unix pipe, etc.
* _input_parameters_: Depends on the input type, but a dictionary of parameters to configure the input adapter

*output_adapter*: Defines a way of moving data produced by the process to the messaging system. A dictionary that can take the following parameters:
* _output_type_: The type of output that the process produces, could be a single file, output read from a port, a file that is appended to, a unix pipe that can be read, etc.
* _output_parameters_: Depends on the output type, but a dictionary of parameters to configure the output adapter


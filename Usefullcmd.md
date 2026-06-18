## Creating and activating venv
    # python -m venv .venv
    # Activating venv
        # Activating on git codespace: source .venv/bin/activate
        # cmd: .venv\Scripts\activate.bat   
        # powershell: .venv\Scripts\Activate.ps1
        # git bash: source .venv/Scripts/activate

## production best practices
1) Never run pip install -r requirement.text directly
2)  i) instead , we can install pip-tools
    ii) we can write our base packages there( I mean we can right something like langgraph>=0.2.0,<0.3.0 : which means that, the python should not go against our contstraints while generating requirement.txt.)
    iii) then we run pip-compile requirement.in, It will generate a in-depth requirement.txt.
    iv) then we can do pip install -r requirement.txt

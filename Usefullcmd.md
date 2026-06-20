## Creating and activating venv
    # python -m venv .venv
    # Activating venv
        # Activating on git codespace: source .venv/bin/activate
        # cmd: .venv\Scripts\activate.bat   
        # powershell: .venv\Scripts\Activate.ps1
        # git bash: source .venv/Scripts/activate

    # [USE THIS] Combined command: use this : 
            python3 -m venv .venv source .venv/bin/activate

# Creating UV commands [ BETTER THAN PIP]
    # pip install uv
    # To compile requirements.in : uv pip compile requirements.in -o requirements.txt
    # to install the requiremetns.txt: uv pip install -r requirements.txt

    # cache clean : uv cache clean
                  : pip cache purge
## production best practices
1) Never run pip install -r requirement.text directly
2)  i) instead , we can install pip-tools
    ii) we can write our base packages there( I mean we can right something like langgraph>=0.2.0,<0.3.0 : which means that, the python should not go against our contstraints while generating requirement.txt.)
    iii) then we run pip-compile requirement.in, It will generate a in-depth requirement.txt.
    iv) then we can do pip install -r requirement.txt

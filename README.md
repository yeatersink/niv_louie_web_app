#Welcome
##Setup

1. run:

```
python -m venv .venv
```

2. Now run:

```
.venv/scripts/activate
```

3. To install the dependancies run:

```
pip install -r requirements.txt
```

---

##Building Installer

1. Create exe file:

```
pyinstaller niv_louie.spec
```

2. run the Create-installer.iss using inno.

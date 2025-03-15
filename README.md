**README for flask/sql setup**

*I am using a conda environment, should also work with venv if you are not using conda*

#create the environment

```
conda create -n flasksqlenv python=3.9
```

#activate the environment

```
conda activate flasksqlenv
```

#install packages

```
conda install flask flask_sqlalchemy
```

*make sure you choose the correct interpreter in VSCode*

#you can also install the packages from the requirements.txt file

```
pip install -r requirements.txt
```

*when everythin is set up, run:* 

```
python run.py
```

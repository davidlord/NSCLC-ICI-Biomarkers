eval "$(conda shell.bash hook)"
conda activate
conda create -n biolung_python python=3.8
conda activate biolung_python
which python
#virtualenv -p python3.8 venv
#source ./venv/bin/activate
python -m pip install -U pip
pip install -r ./requirements.txt
conda deactivate

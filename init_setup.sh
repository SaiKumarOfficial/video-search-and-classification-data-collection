echo [$(date)]: "START"
echo [$(date)]: "Creating conda env with python 3.9" # change py version as per your need
conda create --prefix ./datacollection python=3.9 -y
echo [$(date)]: "activate datacollection"
source activate ./datacollection
echo [$(date)]: "installing the requirements" 
pip install -r requirements.txt
echo [$(date)]: "END" 
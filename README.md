# Welcome to my Washoe County Housing Data Project. # 

This project is inspired by my thesis which I wrote back in 2018 and I wanted 
to revisit the data in Python and see what the last two years of housing
data in Reno/Sparks looks like.  Of course right now the Coronavirus is also
making an impact in the housing market that will be interesting to see. 

Components of this project:
- [x] Download the data from website
- [x] Elongate and clean
- [ ] Generate the same graphs from my thesis but with recent data added
- [ ] Export PDF report of all graphs from my thesis

## How to download and run this project ##

Git clone the repo and install dependencies in a virtual env from requirements.txt
```python
pip install -r requirements.txt
```

Then to run simply
```python
python3 -m app
```

If you would like to stop the app at anytime, simply import IPython.embed
and place ```embed()``` where you want to stop the app for review. It may
also help to turn debug on in the app.py file by ```execute(debug=True)```
as this will save the files and vastly reduce the development timeline. 
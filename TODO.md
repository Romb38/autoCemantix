<h1 align="center">Road Map</h1>

You can find here things that I want to add to my solver :

## 📊 Adding statistics

Currently, this script logs the following things :
- Solver execution time
- Requests numbers

I want to save these number to let user users get stats easily. It will be linked to a command such as `python3 main.py stats`

## 🧼 Update dictionaries daily

My script run at home on a server. I want to update the following everyday :
- `src/resources/frWac.bin` : Model for Cemantix, removing invalid words everyday
- `src/resources/invalid_words.pkl` : List of invalid words found using the script
- Update solver statistics on GitHub everyday (when the fist point is implemented)

I know that is a configuration of my server, but I want to include this on the repository to let users know how to do it.

## ❓ Using randomness on solver

After discussion of the project with some friends, they suggested me to use randomness at the beginning of the script to get a bigger starting point and converge more efficiently. It will be tested when some statistics will be saved.

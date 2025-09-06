<h1 align="center">Road Map</h1>

You can find here things that I want to add to my solver :

## 🔔 Ntfy commands

I know that you can push notification on ntfy server by using only `curl`. I need to adapt my script to remove ntfy script dependency.

## ❓ Using randomness on solver

After discussion of the project with some friends, they suggested me to use randomness at the beginning of the script to get a bigger starting point and converge more efficiently. It will be tested when some statistics will be saved.

## 📊 Show statistics to users

I save some statistics while this script is running (c.f. : README.md). I need to find a way to share these with the world without saving it in the GitHub repository.
I wish to show :
- A graph of `invalid_word_removed_count` as a function of day.
- A graph of `solving_time` as a function of day (with `api_delay` in the title)
- A graph of `requests_count` as a function of day.

## 🧼 Update dictionaries daily - DONE in 082ca5e

My script run at home on a server. I want to update the following everyday :
- `src/resources/frWac.bin` : Model for Cemantix, removing invalid words everyday
- `src/resources/invalid_words.pkl` : List of invalid words found using the script
- Update solver statistics on GitHub everyday (when the fist point is implemented) - Will not be implemented as so

I know that is a configuration of my server, but I want to include this on the repository to let users know how to do it.

## 📊 Adding statistics - DONE in a6c0279

Currently, this script logs the following things :
- Solver execution time
- Requests numbers

I want to save these number to let user users get stats easily. It will be linked to a command such as `python3 main.py stats`

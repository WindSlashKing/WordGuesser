# WordGuesser
A program that outputs answers to crossword puzzles.

## Usage
You tell the program how many letters the word contains as well as the possible letters. You can also specify the positions of characters.
The program then gives you all valid bulgarian words that satisfy the given conditions.

## The algorithm used
In the Data folder there is a JSON file filled with every valid bulgarian word (that I could gather using the scrapers in the "Scrapers" folder).
The program uses a hashmap to build a score for each word in the dictionary. 
The score is calculated by counting how many of the input characters are present in each word in the dictionary.
The hashmap is then filtered and sorted. The remaining items in the hashmap are the final result that is outputted in the console.

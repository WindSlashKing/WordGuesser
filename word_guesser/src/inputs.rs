use std::io::{self, Write};

pub fn get_word_input() -> String {
    println!("Enter the letters the word can contain");
    print!("> ");
    let mut input = String::new();
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut input).unwrap();
    let scrambled_word: String = input.trim_end_matches('\n').to_lowercase();
    scrambled_word
}

pub fn get_length_input() -> usize {
    println!("Enter the length of the word");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let length: usize = input.trim().parse().unwrap();
    length
}
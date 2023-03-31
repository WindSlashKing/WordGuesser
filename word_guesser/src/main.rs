use std::collections::{HashMap, HashSet};
use std::io::{self, Read};
use std::process::exit;
use std::time::Instant;

mod inputs;

fn main() {
    inputs::allow_cyrillic_in_console();
    let word_length = inputs::get_length_input();
    let scrambled_word = inputs::get_word_input();
    let position_letter_map = inputs::get_additional_word_info();

    let file_path = r"..\Data\all_bulgarian_words.json";
    let dictionary = parse_json(file_path);

    let start_time = Instant::now();
    
    let scoreboard: HashMap<String, usize> = create_scoreboard(&scrambled_word, dictionary);
    
    let scoreboard = sort_scoreboard(scoreboard);
    
    let filtered_scoreboard = filter_scoreboard(scoreboard, &scrambled_word, word_length, position_letter_map);
    
    let elapsed_time = start_time.elapsed();
    
    for answer in filtered_scoreboard.keys() {
        println!("{answer}");
    }

    if !filtered_scoreboard.is_empty() {
        println!("Got answers in {:.2}s", elapsed_time.as_secs_f32());
    } else {
        println!("No answers were found");
    }
    exit_program();
}

fn parse_json(file_path: &str) -> HashSet<String> {
    let json_data = std::fs::read_to_string(file_path).unwrap();
    let dictionary: HashSet<String> = serde_json::from_str(&json_data).unwrap();
    dictionary
        .into_iter()
        .map(|word| word.to_lowercase())
        .collect()
}

fn create_scoreboard(scrambled_word: &str, dictionary: HashSet<String>) -> HashMap<String, usize> {
    let mut scoreboard: HashMap<String, usize> = HashMap::new();
    for word in dictionary.iter() {
        let word_score = get_contained_chars_count(scrambled_word, word);
        scoreboard.insert(word.to_owned(), word_score);
    }
    scoreboard
}

fn sort_scoreboard(scoreboard: HashMap<String, usize>) -> HashMap<String, usize> {
    let mut sorted_vec: Vec<(String, usize)> = scoreboard.into_iter().collect();
    sorted_vec.sort_by(|a, b| a.1.cmp(&b.1));
    sorted_vec.into_iter().collect::<HashMap<String, usize>>()
}

fn filter_scoreboard(scoreboard: HashMap<String, usize>, scrambled_word: &str, length: usize, position_letter_map: Option<HashMap<u8, char>>) -> HashMap<String, usize> {
    let mut filtered_scoreboard: HashMap<String, usize> = scoreboard
        .into_iter()
        .filter(|(k, _)| k.chars().count() == length)
        .filter(|(k, _)| k.chars().all(|c| scrambled_word.contains(c)))
        .filter(|(k, _)| k.chars().all(|c| count_char_instances(k, c) <= count_char_instances(scrambled_word, c)))
        .collect();

    if let Some(letter_map) = position_letter_map {
        for (position, letter) in letter_map {
            filtered_scoreboard.retain(|word, _| {
                word.chars().nth((position as usize) - 1).unwrap() == letter
            });
        }
    }
    filtered_scoreboard
}

fn count_char_instances(string: &str, character: char) -> usize {
    string
        .chars()
        .filter(|char| char == &character)
        .count()
}

fn get_contained_chars_count(string: &str, dictionary_word: &str) -> usize {
    let mut count: usize = 0;
    for char in string.chars() {
        if dictionary_word.contains(char) {
            count += 1;
        }
    }
    count
}

fn exit_program() {
    // hold a single byte of input
    let mut buffer = [0; 1];
    println!("Press any key to exit...");
    io::stdin().read_exact(&mut buffer).unwrap();
    exit(0);
}


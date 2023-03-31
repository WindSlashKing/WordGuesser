use std::{io::{self, Write}, collections::HashMap};
use std::process::Command;

pub fn allow_cyrillic_in_console() {
    Command::new("cmd")
        .args(["/C", "chcp", "855", ">", "nul"])
        .output()
        .expect("Failed to execute command");
}

pub fn get_word_input() -> String {
    println!("Въведете буквите, които думата може да съдържа");
    print!("> ");
    let mut input = String::new();
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut input).unwrap();
    let scrambled_word: String = input.trim_end_matches('\n').to_lowercase();
    scrambled_word
}

pub fn get_length_input() -> usize {
    println!("Колко букви има думата?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let length: usize = input.trim().parse().unwrap();
    length
}

pub fn get_additional_word_info() -> Option<HashMap<u8, char>> {
    println!("Искате ли да напишете местата на някои от буквите? (да/не)");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    if !input.to_lowercase().contains('д') {
        return None;
    }

    let mut position_letter_map: HashMap<u8, char> = HashMap::new();
    loop {
        let mut input = String::new();
        
        println!("Въведете буква, която е в думата");
        print!("> ");
        io::stdout().flush().unwrap();
        io::stdin().read_line(&mut input).unwrap();
        let letter = input.chars().next().unwrap();

        println!("Въведете позицията на буквата");
        print!("> ");
        io::stdout().flush().unwrap();
        input.clear();
        io::stdin().read_line(&mut input).unwrap();
        let position: u8 = input.trim().parse().unwrap();
        position_letter_map.insert(position, letter);

        println!("Искате ли да въведете още букви? (да/не)");
        print!("> ");
        io::stdout().flush().unwrap();
        input.clear();
        io::stdin().read_line(&mut input).unwrap();
        if !input.to_lowercase().contains('д') {
            break;
        }
    }
    Some(position_letter_map)
}
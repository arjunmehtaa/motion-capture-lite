#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on Windows in release

use std::net::{UdpSocket, SocketAddr};
use std::thread;
use std::time::Duration;
use concurrent_queue::ConcurrentQueue;
use std::sync::Arc;


fn send_messages(sending_udp_port: u16) {
    let tag_hosts = vec!["192.168.0.12", "192.168.0.13"];
    let beamer_hosts = vec!["192.168.0.11", "empty", "empty"];
    let NUM_BEAMERS = 3;

    thread::sleep(Duration::from_millis(1000));
    let mut counter = 0;
    let NUM_LEDS = 6;
    println!("starting send thread");

    let mut beamer_id = 0;
    let mut udp_hosts = tag_hosts.clone();
    while true {
        udp_hosts.push(beamer_hosts[beamer_id]);
        beamer_id = (beamer_id + 1) % beamer_hosts.len();
        println!("UDP hosts: {:?}", udp_hosts);
        for udp_host in &udp_hosts {
            if *udp_host == "empty" {
                continue
            }
            let socket = UdpSocket::bind(format!("0.0.0.0:{}", sending_udp_port)).expect("Failed to bind socket");
            socket.set_nonblocking(true).expect("Failed to set non-blocking");
            let msg = counter.to_string();
            socket.send_to(msg.as_bytes(), format!("{}:{}", udp_host, sending_udp_port))
                .expect("Failed to send message");
        }
        udp_hosts.pop();
        counter = (counter+1) % NUM_BEAMERS;
        thread::sleep(Duration::from_millis(70));
    }
}

fn message_handler(q: &ConcurrentQueue<(String, SocketAddr)>) {
    loop {
        if !q.is_empty() {
            let pair = q.pop().unwrap();
            let values: Vec<i32> = pair.0.split_whitespace().map(|s| s.parse().unwrap()).collect();
            // print values to console with each digit being padded to 3 spaces

            let padded_values: Vec<String> = values.iter().map(|&num| format!("{:03}", num)).collect();
            println!("{} : {:?} ", pair.1, padded_values);
        }
    }
}

fn receive_messages(listening_udp_port: u16, q: &ConcurrentQueue<(String, SocketAddr)>) {
    // println!("starting recv thread");
    let socket = UdpSocket::bind(format!("0.0.0.0:{}", listening_udp_port)).expect("Failed to bind socket");
    socket.set_nonblocking(true).expect("Failed to set non-blocking");
    let mut buffer = [0; 1024];
    loop {
        match socket.recv_from(&mut buffer) {
            Ok((size, addr)) => {
                let data = String::from_utf8_lossy(&buffer[..size]);
                let _ = q.push((data.to_string(), addr));
                // println!("Received Messages: {} from {}", data, addr);
            }
            Err(_) => {
            }
        }
    }
}

fn main() {
    // let udp_hosts = vec!["192.168.0.11"];
    let sending_udp_port = 4210;
    let listening_udp_port = 5000;

    println!("Hello send thread");

    let message_queue: Arc<ConcurrentQueue<(String, SocketAddr)>> = Arc::new(ConcurrentQueue::unbounded());

    let queue_clone = Arc::clone(&message_queue);
    // let receive_thread = thread::spawn(move || receive_messages(listening_udp_port, &queue_clone));

    let queue_clone = Arc::clone(&message_queue);
    // let handle_received_value = thread::spawn(move || message_handler(&queue_clone));

    let send_thread = thread::spawn(move || send_messages(sending_udp_port));

    send_thread.join().expect("Send thread panicked");
    // receive_thread.join().expect("Receive thread panicked");
    // handle_received_value.join().expect("message handler thread panicked");
}
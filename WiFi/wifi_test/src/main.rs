#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::net::{UdpSocket, SocketAddr};
use std::sync::Arc;
use concurrent_queue::ConcurrentQueue;
use tokio::net::UdpSocket as TokioUdpSocket;
use tokio::time::{sleep, Duration};

async fn send_packet(socket: Arc<UdpSocket>, addr: SocketAddr) {
    let buf = b"Hello, UDP!";
    match socket.send_to(buf, addr) {
        Ok(_) => println!("Sent packet to {}", addr),
        Err(e) => eprintln!("Failed to send packet: {}", e),
    }
}

async fn send_to_multiple_addresses(udp_hosts: Vec<&str>, sending_udp_port: u16) {
    let socket = Arc::new(UdpSocket::bind("0.0.0.0:0").expect("Failed to bind socket"));

    loop {
        let tasks = udp_hosts.iter().map(|&host| {
            let socket_clone = Arc::clone(&socket);
            let addr: SocketAddr = format!("{}:{}", host, sending_udp_port).parse().expect("Invalid address");
            tokio::spawn(send_packet(socket_clone, addr))
        });

        futures::future::join_all(tasks).await;

        // Add a small delay before sending the next batch of packets
        sleep(Duration::from_secs(1)).await;
    }
}

fn message_handler(q: &ConcurrentQueue<(String, SocketAddr)>) {
    loop {
        if !q.is_empty() {
            let pair = q.pop().unwrap();
            println!("{}, {}", pair.0, pair.1);
        }
    }
}

async fn receive_messages(listening_udp_port: u16, q: Arc<ConcurrentQueue<(String, SocketAddr)>>) {
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
            Err(_) => {}
        }
        sleep(Duration::from_millis(10)).await; // Add a small delay to prevent busy looping
    }
}

#[tokio::main]
async fn main() {
    let udp_hosts = vec!["192.168.0.11", "192.168.0.12"];
    let sending_udp_port = 4210;
    let listening_udp_port = 5000;

    let message_queue: Arc<ConcurrentQueue<(String, SocketAddr)>> = Arc::new(ConcurrentQueue::unbounded());

    let queue_clone = Arc::clone(&message_queue);
    let receive_task = receive_messages(listening_udp_port, queue_clone);

    let queue_clone = Arc::clone(&message_queue);
    let handle_received_value = tokio::spawn(async move { message_handler(&queue_clone) });

    let send_task = send_to_multiple_addresses(udp_hosts, sending_udp_port);

    tokio::select! {
        _ = send_task => println!("Send task completed"),
        _ = receive_task => println!("Receive task completed"),
        _ = handle_received_value => println!("Handle received value task completed"),
    }
}

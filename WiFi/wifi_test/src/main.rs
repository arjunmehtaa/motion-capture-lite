#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on Windows in release

use std::net::{UdpSocket, SocketAddr};
use std::thread;
use std::time::Duration;
use concurrent_queue::ConcurrentQueue;
use std::sync::Arc;
use std::sync::Mutex;
use std::sync::RwLock;
use eframe::egui;


fn send_messages(udp_hosts: Vec<&str>, sending_udp_port: u16) {
    thread::sleep(Duration::from_millis(1000));
    let mut counter = 0;
    println!("starting send thread");
    while counter < 101 {
        for udp_host in &udp_hosts {
            let socket = UdpSocket::bind(format!("0.0.0.0:{}", sending_udp_port)).expect("Failed to bind socket");
            socket.set_nonblocking(true).expect("Failed to set non-blocking");
            let msg = counter.to_string();
            socket.send_to(msg.as_bytes(), format!("{}:{}", udp_host, sending_udp_port))
                .expect("Failed to send message");
        }
        counter += 1;
        thread::sleep(Duration::from_millis(80));
    }
}

fn message_handler(q: &ConcurrentQueue<(String, SocketAddr)>, state: Arc<RwLock<GuiState>>) {
    loop {
        if !q.is_empty() {
            let pair = q.pop().unwrap();
            println!("Received Messages: {} from {}", pair.0, pair.1);
            {
                let mut state = state.write().unwrap();
                state.value = pair.0;    
            }

        }
    }
}

fn receive_messages(listening_udp_port: u16, q: &ConcurrentQueue<(String, SocketAddr)>) {
    println!("starting recv thread");
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
    }
}

fn main() {
    let udp_hosts = vec!["192.168.0.11", "192.168.0.12"];
    let sending_udp_port = 4210;
    let listening_udp_port = 5001;

    let gui_state = Arc::new(RwLock::new(GuiState {
        value: "".to_string(),
    }));

    let message_queue: Arc<ConcurrentQueue<(String, SocketAddr)>> = Arc::new(ConcurrentQueue::unbounded());

    let queue_clone = Arc::clone(&message_queue);
    let receive_thread = thread::spawn(move || receive_messages(listening_udp_port, &queue_clone));

    let queue_clone = Arc::clone(&message_queue);
    let handler_state_clone = Arc::clone(&gui_state);
    let handle_received_value = thread::spawn(move || message_handler(&queue_clone, handler_state_clone));

    let send_thread = thread::spawn(move || send_messages(udp_hosts, sending_udp_port));



    env_logger::init(); // Log to stderr (if you run with `RUST_LOG=debug`).
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([320.0, 240.0]),
        ..Default::default()
    };
    let state_clone = Arc::clone(&gui_state);
    eframe::run_native(
        "My egui App",
        options,
        Box::new(|cc| {
            Box::<MyApp>::new(MyApp { gui_state: state_clone })
        }),
    );

    send_thread.join().expect("Send thread panicked");
    receive_thread.join().expect("Receive thread panicked");
    handle_received_value.join().expect("message handler thread panicked");
}

struct MyApp {
    gui_state: Arc<RwLock<GuiState>>,
}
struct GuiState {
    value: String, // Store received messages to display in GUI
}
impl Default for MyApp {
    fn default() -> Self {
        Self {
            gui_state: Arc::new(RwLock::new(GuiState {
                value: "".to_string()
            }))
       }
    }
}

impl eframe::App for MyApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("My egui Application");
            
            let state = self.gui_state.read().unwrap();

            ui.label(format!("value {}", state.value));
        });
    }
}
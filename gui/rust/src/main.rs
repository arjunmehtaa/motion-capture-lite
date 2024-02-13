use std::{
    sync::{Arc, Mutex},
    thread,
    time::{Duration, Instant},
};
use crossbeam_channel::{unbounded, Receiver};

use eframe::egui;

fn main() {
    let options = eframe::NativeOptions::default();
    let app = MyApp::default();
    let _ = eframe::run_native("Test", options, Box::new(move |_cc| Box::new(app)));
}

struct MyApp {
    field: i128,
    rx: Receiver<()>, // Receiver for the channel
}

impl Default for MyApp {
    fn default() -> Self {
        let (tx, rx) = unbounded(); // Create a channel for communication between threads
        let app = MyApp {
            field: 0,
            rx,
        };

        // Spawn a thread to emit signals through the channel
        thread::spawn(move || {
            let mut last_emit = Instant::now();
            loop {
                thread::sleep(Duration::from_millis(10)); // Sleep for shorter duration for more frequent signals
                if last_emit.elapsed() >= Duration::from_millis(500) {
                    // Check if 1 second has passed since last emit
                    if tx.send(()).is_err() {
                        break; // Exit the loop if sending fails (receiver dropped)
                    }
                    last_emit = Instant::now(); // Update last emit time
                }
            }
        });

        app
    }
}

impl eframe::App for MyApp {
    fn update(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame) {
        // Check for signals from the channel and update the value accordingly
        if let Ok(_) = self.rx.try_recv() {
            self.field += 1; // Update the value in response to the signal
        }
        egui::CentralPanel::default().show(ctx, |ui| ui.label(format!("{}", self.field)));
        // std::thread::sleep(std::time::Duration::from_millis(100));
        ctx.request_repaint(); // Request a repaint to update the UI

    }
}
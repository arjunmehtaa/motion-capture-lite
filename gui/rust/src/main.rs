use std::{
    thread,
    time::{Duration, Instant},
};
use crossbeam_channel::{unbounded, Receiver};

use eframe::egui;
use egui_plot::{Plot, PlotPoints, Line};

fn main() {
    let options = eframe::NativeOptions::default();
    let app = MyApp::default();
    let _ = eframe::run_native("Test", options, Box::new(move |_cc| Box::new(app)));
}

struct MyApp {
    field: i128,
    rx: Receiver<()>,
}

impl Default for MyApp {
    fn default() -> Self {
        let (tx, rx) = unbounded();
        let app = MyApp {
            field: 0,
            rx,
        };

        // SENDING SIGNALS: Spawn a thread to emit signals through the channel
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

// RECEIVING SIGNALS AND UPDATING THE UI
impl eframe::App for MyApp {

    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Check for signals from the channel and update the value accordingly
        if let Ok(_) = self.rx.try_recv() {
            self.field += 1; // Update the value in response to the signal
        }
        egui::CentralPanel::default().show(ctx, |ui| {
                ui.label(format!("{}", self.field));

                ui.horizontal(|ui| {
                    Plot::new("Field Value Over Time").height(200.0).show(ui, |ui| {
                        ui.line(Line::new(PlotPoints::new(vec![[0.0, 0.0], [0.5, self.field as f64]])));
                    });
                });
            });
        ctx.request_repaint(); // Request a repaint to update the UI
    }
}
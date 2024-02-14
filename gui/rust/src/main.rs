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
    points: Vec<[f64; 2]>,
}

impl Default for MyApp {
    fn default() -> Self {
        let (tx, rx) = unbounded();
        let app = MyApp {
            field: 0,
            rx,
            points: vec![[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
        };

        // SENDING SIGNALS: Spawn a thread to emit signals through the channel
        thread::spawn(move || {
            let mut last_emit = Instant::now();
            loop {
                thread::sleep(Duration::from_millis(100)); // Sleep for shorter duration for more frequent signals
                if last_emit.elapsed() >= Duration::from_millis(100) {
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

            self.points.remove(0);
            // generate a random number betwee 0 and 64
            self.points.push([(rand::random::<f64>() * 8.0).round(), (rand::random::<f64>() * 8.0).round()]);
        }
        egui::CentralPanel::default().show(ctx, |ui| {
                
                ui.label(format!("Count: {}, Previous Point: {},{} , Current Point: {},{}", self.field, self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1]));
                
                ui.horizontal(|ui| {
                    Plot::new("Field Value Over Time")
                        .height(500.0).width(500.0)
                        // include_x and include_y are used to set the range of the plot
                        .include_x(0.0) .include_x(10.0)
                        .include_y(0.0).include_y(10.0)
                        .allow_drag(false).allow_scroll(false).allow_zoom(false)
                        .view_aspect(1.0) // forces the plot to be square
                        .data_aspect(1.0)
                        .show(ui, |ui| {
                            ui.line(Line::new(PlotPoints::new(self.points.clone())));
                        });
                });
            });
        ctx.request_repaint(); // Request a repaint to update the UI
    }
}
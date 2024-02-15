use std::{
    thread,
    time::{Duration, Instant},
};
use crossbeam_channel::{unbounded, Receiver};

use eframe::egui;
use egui_plot::{Line, Plot, PlotPoints, Points};

fn main() {
    let options = eframe::NativeOptions::default();
    let app = MyApp::default();
    let _ = eframe::run_native("Visualization Demo", options, Box::new(move |_cc| Box::new(app)));
}

struct MyApp {
    field: i128,
    rx: Receiver<()>,
    points: Vec<[f64; 3]>,
}

const BASIC_POINT_ARR: [[f64; 3]; 5] = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]];

impl Default for MyApp {
    fn default() -> Self {
        let (tx, rx) = unbounded();
        let app = MyApp {
            field: 0,
            rx,
            points: BASIC_POINT_ARR.to_vec()
        };

        // SENDING SIGNALS: Spawn a thread to emit signals through the channel
        thread::spawn(move || {
            let mut last_emit = Instant::now();
            loop {
                thread::sleep(Duration::from_millis(500)); // Sleep for shorter duration for more frequent signals
                if last_emit.elapsed() >= Duration::from_millis(500) {
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
            self.points.push([(rand::random::<f64>() * 8.0).round(), (rand::random::<f64>() * 8.0).round(), (rand::random::<f64>() * 8.0).round()]);
        }
        egui::CentralPanel::default().show(ctx, |ui| {
                let (all_but_last, _) = self.points.split_at(self.points.len() - 1);
                let (_, last_two) = self.points.split_at(self.points.len() - 2);

                let all_but_last_2d = all_but_last.iter().map(|x| [x[0], x[1]]).collect::<Vec<[f64; 2]>>();
                let all_but_last_z = all_but_last.iter().map(|x| x[2]).collect::<Vec<f64>>();
                let last_two_2d = last_two.iter().map(|x| [x[0], x[1]]).collect::<Vec<[f64; 2]>>();
                let last_two_z = last_two.iter().map(|x| x[2]).collect::<Vec<f64>>();

                // println!("{:?}", self.points);
                // println!("{:?}", all_but_last);
                // println!("{:?}", last_two);
                // println!();

                ui.vertical_centered(|ui| {
                    ui.label(format!("Count: {} | Current Point: {},{},{}", self.field, last_two[1][0], last_two[1][1], last_two[1][2]));
                    ui.add_space(10.0);

                    ui.horizontal_centered(|ui| {
                        Plot::new("Field Value Over Time")
                            .height(500.0).width(500.0)
                            .include_x(0.0) .include_x(10.0)  // include_x and include_y are used to set the range of the plot
                            .include_y(0.0).include_y(10.0)
                            .allow_drag(false).allow_scroll(false).allow_zoom(false)
                            .show_background(true)
                            .view_aspect(1.0).data_aspect(1.0)
                            .show(ui, |ui| {
                                ui.line(Line::new(PlotPoints::new(all_but_last_2d.to_vec())));
                                ui.line(Line::new(PlotPoints::new(last_two_2d.to_vec())).color(egui::Color32::BLUE));

                                // Highlight all the points except the last
                                for (i, point) in all_but_last_2d.iter().enumerate() {
                                    ui.points(Points::new(vec![*point]).radius(all_but_last_z[i] as f32).color(egui::Color32::RED));
                                }

                                // Highlight the last point
                                if let Some(last_point) = self.points.last() {
                                    let last_point_2d: [f64; 2] = [last_point[0], last_point[1]];
                                    ui.points(Points::new(vec![last_point_2d]).radius(last_point[2] as f32).color(egui::Color32::BLUE));
                                }
                            });
                        });

                        ui.button("Quit").on_hover_ui(|ui| {
                            ui.label("Quit");
                        }).clicked().then(|| {
                            std::process::exit(0);
                        });
                });
            });
        ctx.request_repaint(); // Request a repaint to update the UI
    }
}
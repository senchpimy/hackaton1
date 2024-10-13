use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct AccionRequest {
    texto: String,
}

#[derive(Serialize)]
struct LoginRequest {
    username: String,
    password: String,
}

#[derive(Deserialize, Debug)]
struct LoginResponse {
    message: String,
}

#[derive(Deserialize, Debug)]
struct AccionResponse {
    // Cambiamos el campo "respuesta" por "convo", que es un vector de pares
    convo: Vec<(String, String)>, // cada par es un emisor y un mensaje
}

#[tauri::command]
fn enviar_accion(texto: String) -> String {
    let client = Client::new();

    let accion_data = AccionRequest { texto };

    // Enviamos la petición y esperamos la respuesta
    let response = client
        .post("http://172.31.99.126:8000/acciones")
        .json(&accion_data)
        .send();

    match response {
        Ok(res) => {
            if res.status().is_success() {
                // Convertir la respuesta a JSON
                let response_json: AccionResponse = res.json().unwrap();

                // Crear una respuesta acumulativa a partir del vector de conversación
                let mut respuesta_acumulada = String::new();
                for (emisor, mensaje) in response_json.convo {
                    respuesta_acumulada.push_str(&format!("{}: {}\n", emisor, mensaje));
                }

                respuesta_acumulada
            } else {
                String::new()
            }
        }
        Err(err) => {
            eprintln!("Error al enviar la acción: {:?}", err);
            String::new()
        }
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![enviar_accion])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

"""

@author: Nicola Inchingolo / Maria Labanca

Analizzare un file JSON estraendo tali informazioni, per ogni elemento del JSON.

per ogni utente:
la lista degli indirizzi IP diversi associati a lui; - fatto
per ogni indirizzo IP diverso quanti eventi sono associati a lui.

"""
import json as js


"Permette l'apertura del file ed il caricamento"
def open_file(name_file: str):
    try:
        with open(name_file, 'r') as json_file:
            return js.load(json_file)
    except FileNotFoundError:
        print(f"ERRORE: Il file '{name_file}' non è stato trovato.")
        exit(1)
    except js.JSONDecodeError:
        print(f"ERRORE: Il file '{name_file}' non contiene un JSON valido.")
        exit(1)
    except Exception as e:
        print(f"ERRORE imprevisto nell'apertura del file: {e}")
        exit(1)

"funzione che associa l'id utente per ogni elemento, andando a generare un set per ogni ID"
def associa_id(log_list: list):
    log_dict = dict()
    for log in log_list:
        log_dict[log[1]] = set()
    return log_dict

"funzione che associa ogni id collegato ad un certo utente ai suoi ip utilizzati, popolando il dizionario con un set di elementi"
def associa_ip(log_dict: dict, log_list: list):
    for element in log_dict.keys():
        for log in log_list:
            if log[1] == element:
                log_dict[element].add(log[7])

"funzione che associa ad ogni ip dell'utente, il numero di eventi associati, definendo un dizionario che associa IP-numero_eventi"
def associa_eventi(log_dict: dict, log_list: list):
    for element in log_dict.keys():
        ip = dict()
        for item in log_dict[element]:
            i = 0
            for log in log_list:
                if log[7] == item:
                    i += 1
            ip[item] = i
        log_dict[element] = ip

"funzione che scrive il risultato"
def write_result():
    try:
        with open("test_result.json", "w") as json_file:
            js.dump(log_dict, json_file, indent=4)
    except PermissionError:
        print("ERRORE: Permessi insufficienti per scrivere il file output.")
        exit(1)
    except Exception as e:
        print(f"ERRORE nella scrittura del file: {e}")
        exit(1)



if __name__ == "__main__":
   #file = '.\\test_data\\test_large.json'
    file = input("Inserisci il percorso del file: ")
    log_list = open_file(file)
    log_dict = associa_id(log_list)
    associa_ip(log_dict, log_list)
    associa_eventi(log_dict, log_list)
    write_result()


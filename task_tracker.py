from datetime import datetime
import json
import os
import re


class Task_Tracker:

    def load_data(self):
        "método que se encarga de abrir el archivo json."
        try:
            with open('data.json', 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            return {}  # Retorna un dict vacío si no contiene nada.

    def save_data(self, data):
        "método que se encarga de guardar los datos pasados como argumento, en el archivo json."
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)  # Se guarda de forma legible con un indentado establecido.

    def add_task(self, argument):
        try:
            # Se carga el archivo y se obtiene sus datos si los contiene
            tasks = self.load_data()

            # Se crea un id incremental automático
            new_id = str(len(tasks) + 1)

            #Se establece la hora y fecha de creación de la tarea desde su momento
            timestamp_creation = datetime.now().strftime("%H:%M %d/%m/%Y")

            # Se crea la tarea
            task = {
                "description": argument,
                "status": "PENDIENTE",
                "timestamp_creation": timestamp_creation,
                "timestamp_updated": ""
            }

            # Se agrega la tarea al diccionario
            tasks[new_id] = task

            # Se guarda la tarea
            self.save_data(tasks)

            print("tarea argegada con éxito.")

        except Exception as e:
            print(f"Error: {e}")

    def update_task(self, task_id, argument):

        try:

            # Se cargan los datos guardados en el json
            tasks = self.load_data()

            # Se toma la hora y fecha en el momento de la modificación
            timestamp_update = datetime.now().strftime("%H:%M %d/%m/%Y")

            # Se establece el nuevo argumento y la hora de su modificación
            if str(task_id) in tasks:
                tasks[str(task_id)]['description'] = argument
                tasks[str(task_id)]['timestamp_updated'] = timestamp_update

            self.save_data(tasks)

            print("Cambios guardados correctamente!")

        except Exception as e:
            print(f"Error: {e}")

    def delete_task(self, task_id):

        try:
            # Se abre el archivo y se cargan sus datos
            tasks = self.load_data()

            if str(task_id) in tasks:

                del tasks[task_id]
                print(f"Tarea {task_id}, eliminada.")
            else:
                print(f"No se ha encontrado la tarea {task_id}")

            self.save_data(tasks)

        except Exception as e:
            print(f"Error: {e}")

    def cli_manager(self):
        "Método que se encarga de manejar nuestra consola de comandos."

        while True:
            input_user = input("@task-cli/> ")
            pattern1 = r"^(add)\s+([^\n]+)$"  # Patrón: Comando-argumento
            pattern2 = r"^(update)\s+(\d+)\s+(.+)$"  # patrón: Comando-id-argumento
            pattern3 = r"^(delete|mark-in-progress|mark-done)\s+(\d+)$"  # Patrón: Comando-id

            # Buscar coincidencia de patrones
            match1 = re.match(pattern1, input_user)

            # Caso 1
            if match1:

                # Se separan los valores correspondientes para su uso
                command = match1.group(1)
                argument = match1.group(2)

                if command == "add":
                    self.add_task(argument)

            # Caso 2
            match2 = re.match(pattern2, input_user)
            if match2:

                # Se separan los valores correspondientes para su uso
                command = match2.group(1)
                task_id = match2.group(2)
                argument = match2.group(3)

                if command == "update":  # Debe actualizar la descripción de la tarea
                    self.update_task(task_id, argument)

            # Caso 3
            match3 = re.match(pattern3, input_user)
            if match3:

                # Se separan los valores correspondientes para su uso
                command = match3.group(1)
                task_id = match3.group(2)

                # Si es eliminar:
                if command == "delete":
                    self.delete_task(task_id)

                # Si quiero marcar una tarea como en prograso:
                elif command == "mark-in-progress":

                    argument = "EN PROGRESO"

                    try:

                        # Se cargan los datos guardados en el json
                        tasks = self.load_data()

                        # Se establece el nuevo argumento y la hora de su modificación
                        if str(task_id) in tasks:
                            tasks[str(task_id)]['status'] = argument

                        # Guardo los cambios
                        self.save_data(tasks)

                        print(f"La terea {task_id}, ha sido marcada como: EN PROGRESO")

                    except Exception as e:
                        print(f"Error: {e}")

                # Si quiero marcar una tarea como terminada
                elif command == "mark-done":

                    argument = "TERMINADA"

                    try:

                        # Se cargan los datos guardados en el json
                        tasks = self.load_data()

                        # Se establece el nuevo argumento y la hora de su modificación
                        if str(task_id) in tasks:
                            tasks[str(task_id)]['status'] = argument

                        # Guardo los cambios
                        self.save_data(tasks)

                        print(f"La terea {task_id}, ha sido marcada como: TERMINADA")

                    except Exception as e:
                        print(f"Error: {e}")

            # Como no cumplen con el patrón las siguientes tareas se realizan aparte, por organización
            if input_user == "list todo":

                tasks = self.load_data()

                if any(task["status"] == "PENDIENTE" for task in tasks.values()):
                    for task_id, task_info in tasks.items():
                        if task_info["status"] == "PENDIENTE":
                            print(f'ID: {task_id}, Descripción: {task_info["description"]}, Estado: {task_info["status"]}')

                else:
                    print("No hay tareas pendientes.")

            if input_user == "list done":

                tasks = self.load_data()

                if any(task["status"] == "PENDIENTE" for task in tasks.values()):
                    for task_id, task_info in tasks.items():
                        if task_info["status"] == "TERMINADA":
                            print(f'ID: {task_id}, Descripción: {task_info["description"]}, Estado: {task_info["status"]}')

                else:
                    print("No hay tareas terminadas.")


            if input_user == "list in-progress":

                tasks = self.load_data()

                if any(task["status"] == "PENDIENTE" for task in tasks.values()):
                    for task_id, task_info in tasks.items():
                        if task_info["status"] == "EN PROGRESO":
                            print(f'ID: {task_id}, Descripción: {task_info["description"]}, Estado: {task_info["status"]}')

                else:
                    print("No hay tareas en progreso.")
    

            # Cerrar CLI
            elif input_user == "exit":
                break


app = Task_Tracker()
app.cli_manager()

### **Ejercicio 1: Crear un grupo de procesos con diferentes tiempos de ejecución**  
- Crea `N` procesos que duerman un tiempo aleatorio y muestren un mensaje al despertar.  
- **Desafío:** Asegúrate de que el proceso padre espere a todos los hijos antes de salir.  

### **Ejercicio 2: Sincronización básica con archivos**  
- Cada proceso hijo debe escribir en un archivo compartido (por ejemplo, `registro.txt`).  
- **Desafío:** Asegurar que las escrituras no se mezclen de forma incorrecta (usa `os.open()` con `O_APPEND` o redirección de salida).  

Si logras hacerlos sin problemas, podemos avanzar al siguiente tema sin inconvenientes.  
Si quieres intentarlos y luego revisar juntos, dime y te ayudo a corregirlos. 😃
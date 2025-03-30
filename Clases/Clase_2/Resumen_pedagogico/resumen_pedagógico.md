### 📌 **Resumen Pedagógico de la Clase**  

Durante esta clase, exploraste el concepto de procesos en sistemas operativos, con un enfoque especial en su creación, sincronización y comunicación. A lo largo de la sesión, trabajaste con los siguientes temas clave:  

1. **Fundamentos de procesos**: Comprendiste cómo los procesos se organizan jerárquicamente en UNIX/Linux y cómo `systemd` gestiona los procesos huérfanos.  
2. **Creación y manejo de procesos**: Experimentaste con `fork()` y `exec()`, comprendiendo cómo se generan nuevos procesos y cómo estos pueden reemplazar su imagen de memoria con otro programa.  
3. **Procesos zombis y huérfanos**: Aprendiste a prevenir procesos zombis con `wait()`, y verificaste cómo `systemd` adopta procesos huérfanos.  
4. **Multiprocesamiento en Python**: Exploraste el módulo `multiprocessing`, que simplifica la creación y gestión de procesos en comparación con `fork()`.  
5. **Comunicación entre procesos (IPC)**: Descubriste `Queue` para intercambiar mensajes entre procesos y comprendiste la necesidad de sincronización.  
6. **Sincronización de procesos**: Implementaste mecanismos como `Lock`, `Event` y `Semaphore` para controlar el acceso a recursos compartidos y evitar condiciones de carrera.  

---

### 📊 **Feedback sobre tu desempeño**  

✅ **Fortalezas**  
- **Razonamiento crítico:** Hiciste preguntas interesantes sobre cómo se manejan los procesos en distintos contextos y lenguajes.  
- **Experimentación activa:** Probaste cada concepto con código propio, lo cual refuerza el aprendizaje.  
- **Comprensión progresiva:** Al inicio tenías dudas sobre `multiprocessing`, pero lograste comprenderlo bien al final.  
- **Buena estructuración de ideas:** Tus respuestas fueron claras y demuestran que organizas bien la información aprendida.  

🔄 **Áreas de mejora**  
- **Profundizar en IPC avanzado**: Aunque comprendiste `Queue`, podrías explorar otros métodos como `Pipe` o `SharedMemory` para casos más avanzados.  
- **Optimización de código**: Algunas implementaciones podrían beneficiarse de menos bloqueos y mayor concurrencia, dependiendo del caso de uso.  
- **Explorar más casos límite**: A veces una condición de carrera o un caso inesperado en la sincronización puede dar errores sutiles. Puedes intentar pruebas más extremas para validar la robustez de tu código.  

---

### 🚀 **Próximos pasos sugeridos**  
Si quieres reforzar aún más lo aprendido, podrías:  
- Implementar un pequeño sistema con múltiples procesos que simulen una tarea real (por ejemplo, procesamiento en paralelo de archivos).  
- Explorar `asyncio` en Python para ver cómo se compara con `multiprocessing` en ciertos casos.  
- Leer sobre otros mecanismos de IPC como `named pipes` o `memory-mapped files`.  

Tu desempeño fue excelente, así que estás listo para avanzar al siguiente tema. ¡Buen trabajo! 🎯
### ¿Qué pasaría si un usuario configura una identidad falsa en Git?
Git no verifica la autenticidad del nombre y correo configurados en el sistema local. Si alguien configura una identidad falsa, los commits aparecerán con ese nombre y correo, lo que puede generar confusión en el equipo. Sin embargo, si el proyecto está alojado en una plataforma como GitHub o GitLab, los commits pueden ser verificados con firmas GPG para garantizar autenticidad. En equipos profesionales, se recomienda firmar los commits con una clave GPG para evitar suplantaciones.

### ¿Qué es una firma GPG y cómo se genera? ¿Quién controla la validez de dichas firmas? ¿Cómo puedo crear mi firma GPG?
Una firma GPG (GNU Privacy Guard) es un mecanismo criptográfico que permite firmar digitalmente commits en Git, garantizando su autenticidad. En plataformas como GitHub, los commits firmados con una clave GPG validada aparecen con una marca de verificación.  

- La validez de una firma GPG la controla la infraestructura de claves GPG. Cada usuario genera un par de claves (una pública y una privada). La clave pública se comparte y permite verificar que una firma fue creada con la clave privada del usuario.  

- Para generar una clave GPG en Linux:  
    ```sh
    gpg --full-generate-key
    ```
    Luego, puedes listar tus claves con:  
    ```sh
    gpg --list-secret-keys --keyid-format=long
    ```
    Y exportar la clave pública para usarla en GitHub o GitLab:  
    ```sh
    gpg --armor --export <tu_key_id>
    ```
    
Cuando generas una clave GPG, esta se almacena en `~/.gnupg/` (tu directorio personal dentro de la carpeta `.gnupg`). No necesitas crearla en un directorio específico manualmente; `gpg` se encarga de gestionarla automáticamente.  

   Para añadir la clave a GitHub:  
   - Ve a **Settings > SSH and GPG keys**.  
   - Selecciona **New GPG Key** y pega la clave pública exportada con:  
     ```sh
     gpg --armor --export <tu_key_id>
     ```  
   - Luego, configura Git para firmar los commits automáticamente:  
     ```sh
     git config --global user.signingkey <tu_key_id>
     git config --global commit.gpgsign true
     ```

### ¿En qué ámbitos se utilizan los controles de versiones centralizados?
Aunque los sistemas centralizados han sido en gran medida reemplazados por Git y otros sistemas distribuidos, todavía se usan en algunos contextos:

- Empresas con alta seguridad: Algunas organizaciones restringen la copia del código en máquinas locales por razones de confidencialidad.
- Proyectos con control estricto: Cuando se requiere una única fuente de verdad y cambios revisados antes de llegar al servidor, se puede preferir un sistema centralizado.
- Sistemas heredados: Algunas empresas mantienen herramientas como SVN (Subversion) o Perforce en proyectos antiguos donde la migración a Git sería costosa o complicada.

### ¿Cómo rastrea git los cambios en los archivos?
Git rastrea cambios en archivos mediante un sistema basado en "instantáneas" (snapshots) en lugar de diferencias (diffs). Cuando realizas un commit, Git toma una captura del estado actual de los archivos en el área de staging y la almacena en su base de datos.  

- Si un archivo no cambia entre commits, Git no lo almacena de nuevo, sino que crea un enlace a la versión anterior.  
- Utiliza un algoritmo de hashing SHA-1 para identificar de forma única cada commit y los cambios asociados.

**¿Qué es una snapshot en Git?**  
   Una **snapshot** es una captura del estado de un proyecto en un momento específico. En lugar de almacenar solo diferencias entre versiones (como hacen los sistemas basados en *diff*), Git almacena una imagen completa del contenido del proyecto en cada commit.

**¿Cómo guarda Git el estado de un archivo?**  
   - Si un archivo no ha cambiado desde el último commit, Git no almacena una nueva copia, sino que crea un **puntero** al archivo anterior.  
   - Si el archivo cambió, Git almacena una nueva versión comprimida de ese archivo.  
   - Cada commit tiene una referencia única (hash SHA-1) que permite identificarlo y reconstruir el estado exacto del proyecto en ese punto.  

**¿Por qué `.git` no crece desmesuradamente a medida que el proyecto avanza?**  
   Git usa varias estrategias para optimizar el almacenamiento:  
   - **Compresión con zlib**: los archivos se almacenan comprimidos, reduciendo el espacio ocupado.  
   - **Almacenamiento eficiente de archivos duplicados**: si un archivo no cambia entre commits, Git solo guarda una referencia en lugar de una copia completa.  
   - **Packfiles**: Git periódicamente empaqueta múltiples objetos en un solo archivo más eficiente, reduciendo la cantidad de archivos individuales en `.git`.  

### **Primer commit y flujo de trabajo en Git**  

#### **Modelo de trabajo en Git**  
Git maneja los archivos en tres estados principales:  
1. **Working Directory (Directorio de trabajo)** → Archivos editados pero no rastreados por Git.  
2. **Staging Area (Área de preparación)** → Archivos listos para ser incluidos en el próximo commit.  
3. **Repository (Repositorio local)** → Archivos confirmados y guardados en la base de datos de Git.  

#### **Ciclo de vida de los archivos en Git**  
- **Untracked**: Archivos que existen en la carpeta pero que Git no rastrea aún.  
- **Modified**: Archivos modificados después del último commit.  
- **Staged**: Archivos agregados con `git add`, listos para el próximo commit.  
- **Committed**: Archivos que ya fueron confirmados en el historial de Git.  

### **Ejercicio práctico: Realizar el primer commit**  
Ejecuta los siguientes comandos dentro de tu repositorio:  

1. Verifica el estado del repositorio:  
   ```sh
   git status
   ```
2. Agrega todos los archivos a la zona de staging:  
   ```sh
   git add .
   ```
3. Realiza el primer commit con un mensaje descriptivo:  
   ```sh
   git commit -m "Estructura inicial del repositorio"
   ```
4. Verifica el historial de commits:  
   ```sh
   git log --oneline
   ```

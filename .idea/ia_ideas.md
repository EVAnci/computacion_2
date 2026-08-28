
Sí: con este índice yo cambiaría un poco el criterio respecto de mi propuesta anterior. El recorrido de la materia va explícitamente desde procesos/IPC y sincronización, pasa por sockets/TCP/UDP/IPv4/IPv6 y termina en `asyncio`, `concurrent.futures` y Celery/sistemas distribuidos.  Por eso, un proyecto fuerte debería permitirte **bajar de nivel cuando quieras demostrar conceptos**, aunque luego uses abstracciones de alto nivel.

Por ejemplo, un proyecto hecho únicamente con FastAPI + Celery + Redis podría funcionar perfectamente, pero probablemente escondería demasiado de lo que aprendieron. En cambio, combinar un protocolo propio sobre sockets con `asyncio`, procesos/threads para trabajo local, IPC y eventualmente Celery te da mucho más para defender oralmente.

### Tu scraper sí puede convertirse en un muy buen final

No descartaría tu servidor de scraping. Lo que haría es cambiar el problema de:

> “dame una URL y te devuelvo contenido/estadísticas”

a algo como:

**Sistema distribuido de monitoreo y detección de cambios en sitios web.**

El usuario registra recursos que quiere vigilar y el sistema periódicamente los descarga, analiza cambios, almacena versiones, calcula estadísticas y notifica eventos interesantes.

Eso abre naturalmente varias capas:

```text
                        IPv4 / IPv6
                   ┌──────────────────┐
                   │ Cliente CLI      │
                   └────────┬─────────┘
                            │ TCP
                            │ protocolo propio
                            ▼
                 ┌──────────────────────┐
                 │ Servidor asyncio     │
                 │ coordinador          │
                 └──────┬────────┬──────┘
                        │        │
                   Queue│        │Unix socket
                        │        ▼
                        │   ┌──────────────┐
                        │   │ proceso DB   │──► SQLite
                        │   └──────────────┘
                        ▼
                ┌───────────────┐
                │ scheduler     │
                └───────┬───────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
       asyncio/http          Celery / workers
       descarga              análisis pesado
                                 │
                       ┌─────────┴─────────┐
                       ▼                   ▼
                  worker host A       worker host B
```

Y ahí aparecen decisiones interesantes:

* `asyncio`: muchas descargas simultáneas, porque son I/O-bound.
* `ProcessPoolExecutor`: análisis CPU-bound local.
* Celery: tareas que deban sobrevivir al proceso coordinador o ejecutarse en otra máquina.
* Redis/RabbitMQ: broker, no simplemente “porque Celery lo necesita”.
* `AF_UNIX`: comunicación del proceso que escribe SQLite con otros procesos locales.
* TCP IPv4/IPv6: interfaz cliente-servidor.
* `Queue`: productor-consumidor y backpressure.
* signals: apagado ordenado.
* SQLite: un único proceso writer evita peleas innecesarias entre workers.
* generadores: procesamiento incremental de resultados grandes.
* Docker Compose: levantar coordinador, broker y workers.

Además, TCP te permite demostrar framing, lecturas parciales, cierre de conexión, timeouts y reintentos, que figuran expresamente en el programa.  Y el requisito IPv4/IPv6 te permite usar `getaddrinfo()`, `AF_INET/AF_INET6`, dual-stack y discutir `IPV6_V6ONLY`. 

Eso ya sería **bastante distinto de tu scraper actual**.

---

## Otras ideas que me parecen particularmente buenas

### 1. Sistema de backups incrementales y deduplicados

Un pequeño “mini Borg/Restic” cliente-servidor.

El cliente analiza un directorio y realiza backups hacia un servidor remoto. Los archivos se dividen en chunks, se calculan hashes y solamente se transmiten bloques que el servidor no tenga.

```text
Directorio
   │
   ├─ threads ── lectura de archivos
   │
   ├─ processes ── hash / compresión
   │
   ▼
 Queue de chunks
   │
 TCP IPv4/IPv6
   │
   ▼
Servidor
   │
   ├── almacenamiento
   └── SQLite metadata
```

Tiene muchísimo material académico:

* TCP y protocolo binario propio.
* framing.
* IPv4 + IPv6.
* `asyncio` atendiendo varios clientes.
* producer/consumer.
* `ThreadPoolExecutor` para disco.
* `ProcessPoolExecutor` para compresión/hash.
* `Queue`, `Event`, `Lock`.
* comparación real threads vs processes.
* reintentos.
* transferencias interrumpidas.
* hashes para evitar duplicados.
* señales y shutdown.
* Unix socket para administración local.

Una feature muy buena para defender sería poder interrumpir un backup y luego continuarlo.

**Ventaja:** muestra muy bien sistemas y networking.

**Desventaja:** Celery entra menos naturalmente. Pero no considero obligatorio usar Celery solamente porque está en el programa.

---

### 2. Plataforma de procesamiento distribuido de archivos

Una especie de mini sistema de “jobs”.

El usuario envía un archivo junto a una operación:

```text
ANALYZE archivo.log
COMPRESS datos.csv
HASH imagen.iso
RESIZE foto.jpg
STATISTICS dataset.csv
```

El servidor recibe las peticiones y decide dónde ejecutar cada trabajo.

Puede tener:

* frontend TCP dual-stack;
* protocolo propio;
* scheduler;
* workers locales con `multiprocessing`;
* workers remotos con Celery;
* SQLite para jobs/resultados;
* Unix socket de administración;
* heartbeat de workers;
* prioridades;
* cancelación;
* estados:
  `QUEUED → RUNNING → COMPLETED / FAILED`.

El desafío interesante no sería transformar el archivo sino el **scheduler**.

Podrías incluso implementar:

```text
CPU-bound       → ProcessPool
I/O-bound       → ThreadPool / asyncio
remoto/pesado   → Celery
```

Eso conecta directamente con uno de los núcleos conceptuales del programa: distinguir I/O-bound, CPU-bound, GIL y elegir entre threads, procesos y corrutinas. 

Probablemente es el proyecto con **mayor cobertura conceptual**, aunque el problema en sí es algo más abstracto.

---

### 3. Sistema distribuido de recolección y análisis de logs

Esta me parece especialmente buena.

Imaginate varias máquinas ejecutando agentes:

```text
 PC A ─────┐
 PC B ─────┼────► Log collector ───► procesamiento ───► SQLite
 PC C ─────┘
```

Los agentes observan archivos como:

```text
/var/log/nginx/access.log
/var/log/syslog
app.log
```

y envían eventos al servidor.

Podrías tener **dos canales**:

```text
TCP
    logs importantes
    entrega confiable

UDP
    métricas periódicas
    heartbeats
    pérdida tolerable
```

Eso justifica TCP y UDP realmente, algo que muchos proyectos terminan usando artificialmente.

El collector podría ser `asyncio`, mientras que workers procesan:

* regex;
* estadísticas;
* agrupamiento;
* detección de anomalías simples;
* compresión;
* generación de reportes.

Un agente local podría comunicarse con otro proceso mediante FIFO o Unix Domain Socket.

Unix Domain Sockets están bastante desarrollados en el programa, incluyendo `SO_PEERCRED` y hasta transferencia de file descriptors mediante `SCM_RIGHTS`. 

**Cobertura:** altísima.

**Complejidad:** razonable.

**Problema real:** muy claro.

De todas las alternativas, esta sería una de mis favoritas.

---

### 4. Sincronizador de archivos entre computadoras

Una especie de Dropbox extremadamente pequeño.

Dos nodos mantienen sincronizado:

```text
~/shared/
```

Cuando aparece/modifica/elimina un archivo, el otro nodo replica el cambio.

Ahí tenés:

* sockets TCP;
* IPv4/IPv6;
* framing;
* múltiples conexiones;
* hashing;
* threads observando filesystem;
* procesos haciendo hash/compression;
* colas;
* locks;
* conflictos;
* metadata SQLite;
* reconexión;
* reintentos;
* shutdown;
* sincronización inicial vs incremental.

Y aparece un problema de sistemas muy interesante:

```text
PC A modifica documento.txt
PC B modifica documento.txt
al mismo tiempo
```

¿Qué hacés?

No necesitás solucionar sistemas distribuidos formalmente. Basta con establecer una política:

```text
last-write-wins

o

crear:
documento.conflict-pc-b.txt
```

Eso genera una excelente discusión oral.

---

### 5. Servicio de descarga distribuida con caché

Un servidor recibe URLs y descarga recursos de Internet para varios clientes, manteniendo una caché compartida.

Por ejemplo:

```text
cliente A ─┐
cliente B ─┼──► servidor de descargas
cliente C ─┘           │
                       ├── caché
                       ├── SQLite
                       └── workers
```

Si cinco clientes solicitan simultáneamente el mismo recurso:

```text
https://example.com/large.iso
```

el sistema realiza **una sola descarga**, mientras cinco consumidores esperan el resultado.

Eso introduce una problemática muy linda de concurrencia:

```text
if URL currently downloading:
    subscribe client
else:
    create download task
```

Necesitás sincronización, Futures, productor-consumidor y control de estado.

Podrías añadir:

* límite global de descargas;
* límite por hostname;
* prioridades;
* cancelación;
* resume;
* caché;
* expiración;
* checksums.

Es conceptualmente bastante elegante.

---

### 6. Sistema distribuido de procesamiento multimedia

El cliente manda audio/video/imágenes y pide operaciones.

Por ejemplo:

```text
thumbnail
compress
convert
extract metadata
calculate perceptual hash
```

La red está en `asyncio`; los trabajos CPU-bound se derivan a processes o Celery.

Funciona muy bien técnicamente, aunque tiene cierto parecido conceptual con el proyecto de anonimización de imágenes que mencionaste. Yo probablemente elegiría otra cosa para diferenciarme.

---

## Una idea menos convencional: daemon local + clientes

También podrías hacer algo deliberadamente Unix.

Por ejemplo, un **gestor de trabajos local/remoto** donde existe:

```text
jobd
```

como daemon.

Los programas locales hablan con él mediante:

```text
AF_UNIX
```

mientras que máquinas remotas usan:

```text
AF_INET / AF_INET6
```

El mismo servicio, dos transportes.

Eso te da una oportunidad muy interesante:

```text
Cliente local
    │
    └── Unix Domain Socket ─────┐

Cliente remoto                  │
    │                           ▼
    └── TCP IPv4/IPv6 ──────► jobd
                                │
                           worker pool
```

Incluso podrías autenticar conexiones locales mediante `SO_PEERCRED`, que aparece específicamente en el temario. 

Académicamente queda muy bonito porque comparás:

> misma semántica de aplicación, distintos dominios/transports.

---

# Las que yo pondría arriba de la mesa

Si las ordenara pensando **no sólo en hacerlas, sino en defenderlas frente al profesor**, quedaría más o menos así:

| Proyecto                | Redes | Concurrencia |   IPC | Async | Celery | Originalidad |     Riesgo |
| ----------------------- | ----: | -----------: | ----: | ----: | -----: | -----------: | ---------: |
| Monitor web distribuido | ★★★★★ |        ★★★★☆ | ★★★★☆ | ★★★★★ |  ★★★★★ |        ★★★★☆ |      Medio |
| Collector de logs       | ★★★★★ |        ★★★★★ | ★★★★★ | ★★★★★ |  ★★★☆☆ |        ★★★★★ |      Medio |
| Backup deduplicado      | ★★★★★ |        ★★★★★ | ★★★★☆ | ★★★★☆ |  ★★☆☆☆ |        ★★★★★ |      Medio |
| Job processing platform | ★★★★☆ |        ★★★★★ | ★★★★★ | ★★★★★ |  ★★★★★ |        ★★★☆☆ |      Medio |
| Sync de archivos        | ★★★★★ |        ★★★★★ | ★★★★☆ | ★★★★☆ |  ★★☆☆☆ |        ★★★★★ |       Alto |
| Download manager/cache  | ★★★★☆ |        ★★★★★ | ★★★☆☆ | ★★★★★ |  ★★★☆☆ |        ★★★★☆ | Bajo/medio |

Mis tres candidatas serían:

**1. Collector distribuido de logs y métricas** si querés que predominen Computación II / sistemas.

**2. Evolución de tu scraper hacia un monitor web distribuido** si querés aprovechar muchísimo código y conocimiento previo pero elevar considerablemente la arquitectura.

**3. Backup incremental/deduplicado** si querés algo muy “de sistemas” y bastante distinto a los proyectos de tus compañeros.

Y hay una cosa importante: **no intentaría meter los 19 bloques del índice**. Por ejemplo, las primitivas `Lock`, `RLock`, `Semaphore`, `Condition`, `Event` y `Barrier` aparecen todas como contenido,  pero utilizar las seis en un mismo proyecto probablemente sería peor diseño que utilizar correctamente `Queue + Event + Lock`.

Me parece mucho más defendible poder decir:

> “Elegí `Event` porque necesitaba comunicar el shutdown; no utilicé `Condition` porque no tengo una condición compleja sobre estado compartido.”

Eso demuestra más comprensión que incluir una `Condition` porque estaba en el programa.

Del mismo modo, `concurrent.futures` te da explícitamente pools de threads y procesos, Futures, cancelación, timeouts y callbacks,  mientras Celery lleva esos conceptos al escenario distribuido mediante productores, workers, broker, estados, retries/composición y escalabilidad horizontal.  Una arquitectura donde **ambos existen por razones distintas** sería particularmente fácil de justificar.

Si yo tuviera que elegir ya mismo con lo que me contaste, probablemente profundizaría primero en **collector de logs**, **monitor web distribuido** y **backup incremental**, porque los tres permiten diseñar una arquitectura interesante sin parecer variantes de los proyectos que ya hicieron tus compañeros.

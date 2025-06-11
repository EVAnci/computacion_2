# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## 0. Diseño general

1. **Generación de datos**: El proceso principal simula datos biométricos en tiempo real, generando 60 muestras (1 por segundo) con campos `frecuencia`, `presion` (tupla sistólica/diastólica) y `oxigeno` (%).
2. **Procesos de análisis**: Cada proceso (`Proc A`, `Proc B`, `Proc C`) recibe los datos completos, extrae su señal, aplica un cálculo costoso (como una función matemática compleja) y devuelve un resultado numérico.

## 1. IPC

### Generador a Analizadores



# Validación de Reply App

Fecha de ejecución: 3 de noviembre de 2026 (America/Guayaquil).

## Compilación y análisis

- JDK utilizado: Eclipse Temurin 17.0.19.
- Gradle oficial: 8.4; AGP 8.1.2; Kotlin 1.9.10.
- `assembleDebug`: BUILD SUCCESSFUL. La primera compilación con descarga de dependencias demoró 6 min 45 s.
- `assembleDebug lintDebug`: BUILD SUCCESSFUL en 1 min 31 s; 37 tareas, 6 ejecutadas y 31 actualizadas.
- Lint: **0 errores y 12 advertencias**. Se conservan los niveles de SDK y recursos oficiales; las advertencias incluyen antigüedad del target SDK, recursos sin usar y configuración del ejemplo. Registro completo: `evidencias/lint.txt`.
- Se instalaron Build Tools 33.0.1 requeridas por el AGP oficial. Las advertencias sobre versiones de XML del SDK no impidieron compilar.
- El primer intento con JBR 25 falló por incompatibilidad con Gradle 8.4. Se retiró la configuración residual que exigía Java 25 y se seleccionó Temurin 17 para la compilación y para Gradle en Android Studio. Esta configuración local no se publica.
- La sincronización real de Android Studio concluyó con `onSuccess(RESOLVE_PROJECT:1)` y `Gradle sync finished` a las 12:02 del 3 de noviembre de 2026, según el registro del IDE. El modelo reconoció Reply_app y JDK_17.

## Ejecución real

- Dispositivo: emulador `Reply_Tablet_API_35`, serial `emulator-5554`, Android 15/API 35.
- Resolución de las evidencias del emulador: 1200 × 1920, densidad 320.
- APK: `app/build/outputs/apk/debug/app-debug.apk`, instalado mediante adb con resultado Success.
- Se ejecutó `python scripts/validar_emulador.py emulator-5554` con **23 comprobaciones satisfactorias**. La lista íntegra está en `evidencias/validacion.json`.
- La prueba verificó subtotales de USD 2, 12 y 24; Next deshabilitado sin selección; habilitación al elegir; cuatro fechas; recargo de USD 3; conservación de cantidad/sabor/fecha/precio; Up; Atrás; Cancel en Flavor/Pickup/Summary; nuevo pedido sin datos residuales; Sharesheet y retorno a Summary.
- Las primeras tentativas estuvieron bloqueadas por un diálogo del sistema del emulador («System UI isn't responding»). Tras reiniciar ese componente, se repitió la prueba completa. Un error inicial del script consultaba el atributo enabled del texto de Next; se corrigió para consultar su contenedor clicable. Estos intentos fallidos no se cuentan entre los resultados satisfactorios.

## Datos compartidos y fidelidad

Sharesheet se identificó mediante su paquete `com.android.intentresolver`. Se conservó el XML real en `evidencias/sharesheet.xml` y una captura del texto y las aplicaciones disponibles. No se eligió un destinatario y no se envió ningún mensaje.

El texto contiene cantidad, sabor y fecha correctos. El campo `Total: 6` reproduce una particularidad de la base oficial: SummaryScreen usa quantity como cuarto argumento de order_details, tanto en starter como en navigation. El subtotal visual sí muestra USD 12. Se documenta el problema y se conserva por la restricción de fidelidad. No se afirma que ese campo compartido represente correctamente el total monetario.

Se comparó con upstream/navigation (`05af7861946a9bd35961eb8554d0559e3dab45fe`). OrderViewModel, OrderUiState, DataSource y CommonUi no tienen diferencias. Se conservaron los modificadores de la solución y las funciones de navegación equivalentes. La identidad solicitada y las diferencias de comentarios/formato son intencionales.

## Git y GitHub

Los commits de implementación son auténticos, incrementales y tienen títulos y cuerpos en español. `docs/historial_git.txt` incluye hash, etapa y explicación técnica. Se revisó git diff --check.

Se creó y publicó un repositorio independiente **privado**, sin sobrescribir repositorios existentes:

https://github.com/diegocalva04/Reply_app_Navigation_Compose

La publicación inicial se verificó mediante git push y la API autenticada de GitHub, que devolvió `private: true`, rama `main` y el commit de implementación `8ed5086adfa6ce0dd2faa7f511b602573b818132`. La documentación y las evidencias se publican en una etapa posterior. `evidencias/github_verificado.json` conserva los metadatos de publicación. No se incluyen credenciales, local.properties, .idea, cachés o el respaldo previo.

## Evidencias disponibles y alcance de verificación

- Seis capturas directas del emulador: inicio, sabor, retiro, resumen, Sharesheet y AppBar. Son capturas originales; no se generaron ni reconstruyeron interfaces.
- Se completó la captura del árbol de paquetes expandido y de las cuatro rutas en Android Studio: `01_estructura.jpg`. La captura anterior de sincronización se conserva como evidencia complementaria.
- Se capturó el panel Git de Android Studio, filtrado por HEAD, con los catorce commits anteriores al cierre de evidencias y la descripción técnica en español de un commit: `08_historial_git.jpg`.
- La captura auténtica de GitHub adjuntada por el usuario se conservó sin modificaciones en `09_github.png`. Muestra la visibilidad privada, main, los archivos publicados y catorce commits. Su SHA-256 coincide con el archivo adjunto original. La publicación también se verificó mediante la API remota.
- Quedaron cubiertas las nueve evidencias visuales solicitadas. La interrupción previa del control de Firefox no afectó a la captura posterior de Android Studio ni a la incorporación de la evidencia de GitHub aportada por el usuario.
- Se verificó visualmente el render de las tres funciones originales `StartOrderPreview`, `SelectOptionPreview` y `OrderSummaryPreview` en Android Studio. Las tres mostraron **Up-to-date**. Las capturas complementarias `10_preview_inicio.jpg`, `11_preview_opciones.jpg` y `12_preview_resumen.jpg` conservan esa comprobación. Se mantuvieron los datos de ejemplo originales y la presentación del panel con límites de diseño; esas vistas previas no sustituyen las pruebas ejecutadas en el emulador.
- Las pruebas cubren el dispositivo, la orientación y los escenarios registrados. No se ejecutaron pruebas exhaustivas sobre todas las versiones, pantallas, recreación de proceso o dispositivos físicos.

El informe utiliza la plantilla p.docx original con portada, encabezados, logotipos, marca de agua, numeración, márgenes y estilos. Se preservaron Calva Diego, Ingeniería de Software y «- / -» para docente/materia. Se actualizó la fecha y el contenido, y se verificó su paginación mediante exportación de Word a PDF y revisión de las imágenes de cada página.

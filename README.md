# Reply App — Práctica de navegación en Compose basada en Cupcake

Implementación del codelab [Cómo navegar entre pantallas con Compose](https://developer.android.com/codelabs/basic-android-kotlin-compose-navigation?hl=es-419), desarrollada progresivamente desde `starter` del [repositorio de Google](https://github.com/google-developer-training/basic-android-kotlin-compose-training-cupcake).

El proyecto Gradle se llama `Reply_app` y el nombre visible es **Reply App**. Conserva el contenido de **Cupcake**, el paquete `com.example.cupcake`, las clases, el diseño, los recursos y el ViewModel oficiales.

## Funcionalidad

Flujo: `Start → Flavor → Pickup → Summary`.

- Cantidades originales: 1, 6 y 12 cupcakes; selección de sabor y fecha con RadioButton.
- Estado compartido mediante `OrderViewModel`, `OrderUiState` y `StateFlow`.
- Navegación centralizada en `CupcakeApp`, con `NavHostController`, `rememberNavController`, `NavHost` y `composable`. Las pantallas individuales reciben callbacks.
- Cancelación mediante `resetOrder()` y `popBackStack(Start.name, inclusive = false)`.
- Compartir con `ACTION_SEND`, `text/plain`, `EXTRA_SUBJECT`, `EXTRA_TEXT` e `Intent.createChooser`.
- AppBar con títulos por destino y botón Up mediante `navigateUp()`.

## Tecnologías de la base oficial

Kotlin 1.9.10, Compose BOM 2023.10.01, Material 3, Navigation Compose 2.7.4, Lifecycle 2.6.2, AGP 8.1.2, Gradle 8.4, JDK 17, compileSdk/targetSdk 34 y minSdk 24.

## Estructura

```text
app/src/main/java/com/example/cupcake/
  MainActivity.kt             # Activity y tema
  CupcakeScreen.kt            # Rutas, NavHost, AppBar, cancelación e intent
  data/                      # DataSource y OrderUiState
  ui/                        # Pantallas y OrderViewModel
  ui/components/CommonUi.kt  # FormattedPriceLabel
  ui/theme/                  # Tema original
docs/                        # Análisis, historial y validación
evidencias/                  # Capturas auténticas y resultados
scripts/validar_emulador.py   # Comprobación real mediante adb
Informe_Reply_App_Navigation_Compose.docx
```

## Ejecutar

Abrir esta carpeta en Android Studio, seleccionar **JDK 17** como Gradle JDK, sincronizar y ejecutar `app`. El JBR 25 de Android Studio reciente no es compatible con el Gradle oficial. Se requiere SDK Android 34 y un dispositivo API 24 o superior.

```powershell
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot'
.\gradlew.bat assembleDebug lintDebug
adb -s emulator-5554 install -r app\build\outputs\apk\debug\app-debug.apk
python scripts\validar_emulador.py emulator-5554
```

El script requiere Python 3, `adb` en PATH, un emulador iniciado y la interfaz oficial en inglés. Guarda capturas y resultados en `evidencias/`. Solo abre Sharesheet; no envía pedidos.

## Resultados verificados el 3 de noviembre de 2026

- `assembleDebug` y `lintDebug`: **BUILD SUCCESSFUL**; lint: **0 errores y 12 advertencias**.
- APK instalado y ejecutado en **Reply_Tablet_API_35**, Android 15/API 35.
- **23 comprobaciones satisfactorias** en `evidencias/validacion.json`: cantidades, precios, selección obligatoria, recorrido, recargo, conservación de datos, Up, Atrás, cancelación desde los tres destinos y Sharesheet.
- Comparación con `upstream/navigation`: navegación equivalente; modelos, ViewModel, datos y componente de precios intactos.
- Historial real en español, publicado en [GitHub privado](https://github.com/diegocalva04/Reply_app_Navigation_Compose).

### Particularidad del ejemplo oficial

En `SummaryScreen.kt`, el cuarto argumento de `order_details` es `orderUiState.quantity`. Por ello, Sharesheet muestra `Total: 6` para seis cupcakes, aunque la pantalla muestra correctamente `Subtotal $12.00`. Este comportamiento de `starter` y `navigation` se conserva por la fidelidad solicitada y queda documentado.

## Documentación y licencia

El informe utiliza la plantilla institucional suministrada y preserva portada, logotipos, marca de agua, márgenes y estilos. Docente y materia permanecen como en la plantilla (`- / -`). El alcance de evidencias y las verificaciones pendientes se especifican en `docs/validacion.md`.

La base oficial conserva su licencia [Apache 2.0](LICENSE) y los avisos de copyright de Google/Android Open Source Project.

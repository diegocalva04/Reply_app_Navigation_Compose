# Análisis y trazabilidad del codelab

Fecha: 3 de noviembre de 2026. Proyecto: Reply_app, nombre visible Reply App, paquete com.example.cupcake.

Fuente: [Cómo navegar entre pantallas con Compose](https://developer.android.com/codelabs/basic-android-kotlin-compose-navigation?hl=es-419).
Código: [repositorio oficial](https://github.com/google-developer-training/basic-android-kotlin-compose-training-cupcake).
Referencias consultadas: starter `4b6bf04748b563e2bef3ee11eb248f32ae6e2882`; navigation `05af7861946a9bd35961eb8554d0559e3dab45fe`.

## 1. Antes de comenzar

Se revisaron los requisitos de Kotlin, lambdas, funciones de alcance y diseños Row y Column. El objetivo es definir destinos, administrar la pila, compartir texto y actualizar la AppBar. Se verificaron Android Studio, SDK, Gradle, JDK 17, Git y una sesión autenticada de GitHub. El proyecto local previo contenía una pantalla Greeting; se respaldó antes de importar starter. No se tomó navigation como punto de partida.

## 2. Código de partida

Se obtuvo starter mediante git fetch y se materializó su árbol directamente en CupcakeApp, sin carpeta anidada. Se mantuvieron LICENSE, recursos y configuración oficial: AGP 8.1.2, Kotlin 1.9.10, Compose BOM 2023.10.01, Navigation Compose 2.7.4, compileSdk/targetSdk 34 y minSdk 24. Navigation Compose ya estaba declarada: no fue necesario añadir otra biblioteca. Se cambió rootProject.name a Reply_app y únicamente app_name a Reply App. Se retiró un archivo residual que exigía Java 25, incompatible con Gradle 8.4. La primera tentativa con ese Java falló; la compilación con JDK 17 tuvo éxito. Commit: preparación y configuración de identidad.

## 3. Explicación de la aplicación

MainActivity configura CupcakeTheme y CupcakeApp. StartOrderScreen y SelectQuantityButton ofrecen las cantidades de DataSource.quantityOptions (1, 6, 12). SelectOptionScreen reutiliza RadioButton para sabores (DataSource.flavors, identificadores de strings) y fechas (pickupOptions de OrderViewModel). OrderSummaryScreen en SummaryScreen.kt presenta cantidad, sabor, fecha, precio y acciones. OrderUiState contiene quantity, flavor, date, price y pickupOptions; OrderViewModel utiliza MutableStateFlow, expone StateFlow y actualiza copias inmutables. FormattedPriceLabel, de CommonUi.kt, conserva el formato de precios. Las tres funciones @Preview originales se conservaron y sus callbacks requeridos se actualizaron. Se revisaron las imágenes de inicio, opciones, resumen y Sharesheet del codelab como referencia, sin incorporarlas a las evidencias propias.

## 4. Rutas, controlador y NavHost

Se creó enum class CupcakeScreen con Start, Flavor, Pickup y Summary; name identifica cada ruta. CupcakeApp recibe OrderViewModel = viewModel() y NavHostController = rememberNavController(). NavHost usa el mismo controlador, startDestination = CupcakeScreen.Start.name y padding(innerPadding) del Scaffold. Cuatro composable registran exactamente los cuatro destinos.

Start recibe quantityOptions y Modifier.fillMaxSize().padding(dimensionResource(R.dimen.padding_medium)). Flavor obtiene LocalContext.current, transforma flavors con map y context.resources.getString, muestra uiState.price y llama setFlavor desde onSelectionChanged. Pickup recibe uiState.pickupOptions y llama setDate. Summary recibe orderUiState = uiState. Las opciones y el resumen conservan fillMaxHeight. La solución navigation añade fillMaxSize y verticalScroll(rememberScrollState()) al NavHost, incorporados durante la comparación final. Imports principales: androidx.navigation.NavHostController; androidx.navigation.compose.NavHost, composable y rememberNavController; layout; LocalContext; dimensionResource. Commits: rutas y contenedor.

## 5. Navegación y pila

StartOrderScreen recibió primero onNextButtonClicked: () -> Unit y luego (Int) -> Unit, con commits auténticos para ambas etapas. Cada botón llama onNextButtonClicked(item.second); item.first conserva la etiqueta. StartOrderPreview proporciona {}. SelectOptionScreen agrega onCancelButtonClicked y onNextButtonClicked, ambos () -> Unit = {}. Cancel y Next ejecutan esos callbacks; enabled = selectedValue.isNotEmpty() permanece intacto. OrderSummaryScreen agrega onCancelButtonClicked: () -> Unit y onSendButtonClicked: (String, String) -> Unit; Send transmite newOrder y orderSummary y la vista previa conserva lambdas vacías.

La lógica centralizada en CupcakeApp llama setQuantity(it) y navigate(Flavor.name), luego navigate(Pickup.name) y navigate(Summary.name). Las pantallas individuales no reciben el controlador. cancelOrderAndNavigateToStart(viewModel, navController) ejecuta resetOrder() y después popBackStack(Start.name, inclusive = false). Los tres botones Cancel usan esa función. Atrás y Up retroceden un destino; Cancel limpia el pedido y elimina todos los destinos posteriores a Start. Pruebas previstas y ejecutadas mediante el script de validación: cantidades, selección obligatoria, recorrido, conservación del pedido y cancelación desde cada destino. Los resultados concretos se registran en evidencias/validacion.json.

## 6. Navegación a otra aplicación

shareOrder(context: Context, subject: String, summary: String) crea Intent(Intent.ACTION_SEND).apply, establece type = "text/plain", agrega EXTRA_SUBJECT y EXTRA_TEXT y llama context.startActivity(Intent.createChooser(intent, context.getString(R.string.new_cupcake_order))). Summary obtiene LocalContext.current y conecta onSendButtonClicked. Imports: android.content.Context e Intent. La prueba abre Sharesheet, inspecciona los datos y regresa sin enviar mensajes ni pedidos a terceros. Commit: Intent ACTION_SEND.

## 7. AppBar que responde a la navegación

CupcakeScreen agrega @StringRes val title: Int: Start usa app_name; Flavor choose_flavor; Pickup choose_pickup_date; Summary order_summary. CupcakeApp observa val backStackEntry by navController.currentBackStackEntryAsState(); CupcakeScreen.valueOf(backStackEntry?.destination?.route ?: CupcakeScreen.Start.name) identifica el destino. CupcakeAppBar recibe currentScreen y utiliza stringResource(currentScreen.title). canNavigateBack = navController.previousBackStackEntry != null controla el icono; navigateUp = { navController.navigateUp() } retrocede. Se conservan colores y estilos de TopAppBar. Imports adicionales: StringRes y currentBackStackEntryAsState. Pruebas: título por destino, ausencia de Up en Start y retorno desde un destino posterior. Commit: AppBar dinámica.

## 8. Solución oficial

Se comparó el trabajo progresivo con upstream/navigation mediante git diff. OrderViewModel.kt, OrderUiState.kt, DataSource.kt y CommonUi.kt permanecen idénticos. Los eventos y la navegación coinciden funcionalmente. Se añadieron los modificadores de desplazamiento y el ancho completo de los botones presentes en navigation. Las diferencias restantes son comentarios, orden de imports, formato, nombre visible y nombre del proyecto. No se reemplazaron archivos por la solución completa.

## 9. Resumen, verificación y errores observables

Se aplican rutas declarativas, callbacks, StateFlow, administración de pila e intents. Los problemas que se comprobaron durante el trabajo incluyen la incompatibilidad de Java 25 con el Gradle oficial y la instalación inicial de Build Tools 33.0.1. Las advertencias del SDK moderno no impidieron compilar.

Existe una particularidad heredada del código oficial: SummaryScreen pasa orderUiState.quantity como cuarto argumento de order_details, aunque la etiqueta dice Total. El subtotal de la pantalla utiliza correctamente orderUiState.price. Se conserva esa instrucción de starter y navigation por la exigencia de fidelidad y se documenta al revisar el contenido compartido; no debe confundirse el subtotal visual con ese campo del texto. No se añaden arquitecturas, pantallas ni funciones ajenas al codelab.

La ejecución y sus límites se detallan en validacion.md. El historial real y los hashes se entregan en historial_git.txt; las capturas se encuentran en evidencias. Además de compilar sus firmas, se inspeccionaron StartOrderPreview, SelectOptionPreview y OrderSummaryPreview renderizadas con estado Up-to-date en Android Studio. Se completaron la estructura de paquetes y el historial Git en pantalla, y se incorporó sin modificaciones la captura de GitHub aportada por el usuario.

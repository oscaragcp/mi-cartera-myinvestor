# Mi cartera MyInvestor

Panel web para analizar una cartera de fondos de MyInvestor a partir del CSV de órdenes que se exporta desde la web del banco: ganancias por año de cuenta, aportaciones, composición, rentabilidad mensual (TWR), TIR y caídas.

- **Panel**: https://oscaragcp.github.io/mi-cartera-myinvestor/
- **Documentación**: https://oscaragcp.github.io/mi-cartera-myinvestor/docs/ (fuente en `docs/index.html`)

- **Privacidad**: el CSV se procesa y se guarda solo en el navegador de quien lo sube. Este repositorio no contiene datos personales (`*.csv` está en `.gitignore`).
- **Valores liquidativos**: `data/navs.json`, actualizado cada día laborable por la acción `Actualizar valores liquidativos` a partir de los fondos de `data/funds.json`. Para añadir un fondo nuevo, añade su ISIN, SecId de Morningstar, nombre y bloque a `data/funds.json`.
- **Tecnología**: HTML + JavaScript sin dependencias de compilación; gráficas con ECharts 5.5.0.

module.exports = {
  content: [
    "./app/templates/**/*.{html,js}",  // Escanea HTML y JS
    "./app/routes.py",                 // Escanea rutas Flask (para clases dinámicas)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
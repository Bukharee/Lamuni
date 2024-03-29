module.exports = {
  content: ["./**/*.{html,js}",
    "./index.html"],
  theme: {
    extend: {
      colors: {
        "light-orange": "#fbf8f3",
        white: "#ffffff",
        "dark-green": "#16a34a",
        "light-gray": "#c7c3c0",
        "dark-gray": "#4f4f4f",
        "dark-orange": "#ff962a",
        "dark-black": "#101010",
        "light-green": "#60af7c",
        "dark-red": "#ef4444",
        "light-color": "bg-slate-100"
      },
      padding: {
        '1/2': '50%',
        full: '100%',
      },
      fontFamily: {
        Poppins: ["Poppins, sans-serif"]
      },
      plugins: [],
    },
  },
}
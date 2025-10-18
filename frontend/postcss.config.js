export default {
  plugins: {
    "postcss-import": {},
    "postcss-nesting": {}, // bu satır önemli — Tailwind'den önce olmalı
    tailwindcss: {},
    autoprefixer: {},
  },
};

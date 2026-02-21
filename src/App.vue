<template>
  <div style="height: 100vh; width: 100vw; user-select: none;">
    <MainPage />
  </div>
</template>

<script>
import MainPage from "@/views/MainPage/MainPage"
export default {
  name: 'App',
  components: {
    MainPage
  },
  mounted() {
    const settings = localStorage.getItem("appSettings");
    if (settings) {
      const parsedSettings = JSON.parse(settings);
      document.documentElement.setAttribute("theme-mode", parsedSettings.themeMode || "light");
    }
  },
}
</script>

<style>
:root[theme-mode="dark"] {
  --td-gray-color-13: #0B0F19;
  --yf-shadow-color-1: #4481e244;
  --yf-color-1: #111C2D;
  --yf-color-2: #4480E2;
  --yf-color-3: #12172b;
  --yf-color-4: transparent;
  --yf-color-5: rgba(255, 255, 255, 0.05);
  --yf-color-6: #ffffff;
  --yf-color-7: var(--yf-color-2);
  --yf-color-8: #3e4d7c;
  --yf-color-9: #222222;
  --yf-color-10: #111111;
}

:root[theme-mode="light"] {
  --yf-shadow-color-1: rgba(0, 0, 0, 0.15);
  --yf-color-1: #F3F6FB;
  --yf-color-2: #0D1427;
  --yf-color-3: #FFFFFF;
  --yf-color-4: #3686CF;
  --yf-color-5: #3a6cbd;
  --yf-color-6: var(--yf-color-4);
  --yf-color-7: var(--yf-color-4);
  --yf-color-8: var(--yf-color-4);
  --yf-color-9: #999999;
  --yf-color-10: #777777;
  --td-gray-color-13: #FFFFFF;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  overflow: hidden;
}

body {
  margin: 0;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(255, 0, 0, 0.15);
  border-radius: 10px;
}
</style>

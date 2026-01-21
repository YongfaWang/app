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
  }
}
</script>

<style>
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
</style>
